import pathlib
import shutil

from utilities.wcmodehandler import WoodchipperCoreModeHandler as WCHandler
from utilities.wcutil import WoodchipperNamespace as WCNamespace
from core.wctk_archive import WoodchipperArchive as WCArchive
from interface.constants import KEY, ERROR, HANDLER, STATE, clr_state
import interface.constants as C
import utilities.wcdiff as WCDiff

class WoodchipperToolkitHandler(WCHandler):
    def __init__(self, request, response, handler=None):
        WCHandler.__init__(self, request, response)
        self.file_name = C.FILE_NAME.ARCHIVE
        if self.request.debug:
            self.file_name = C.FILE_NAME.DEBUG
        self.archive = WCArchive(self.file_name)
        self.archive.load()
        self.handler_function = handler
        self.target_toolkit = None
        self.target_clone = None
        if self.request.target is not None:
            target_pieces = self.request.target.split('/')
            self.target_toolkit = target_pieces[0]
            self.target_clone = target_pieces[1] if len(target_pieces)>1 else None
        self.log_kvp(KEY.RESULTS.HANDLER, HANDLER.GENERIC)
        self.log_kvp(KEY.RESULTS.TARGET, HANDLER.TARGET.ALL)

    def handle(self):
        handler_target = self._handle_clone
        if self.target_toolkit is None:
            self.results.handler = self.handler_function.ALL
            self.results.target = HANDLER.TARGET.ALL
            handler_target = self._handle_all
        elif self.target_clone is None:
            self.results.handler = self.handler_function.TOOLKIT
            self.results.target = HANDLER.TARGET.TOOLKIT
            handler_target = self._handle_toolkit
        else:
            self.results.handler = self.handler_function.CLONE
            self.results.target = HANDLER.TARGET.CLONE
            handler_target = self._handle_clone
        handler_result = handler_target()
        self.archive.save()
        return handler_result

    def _claim_toolkit(self):
        data = None
        success = False
        if self.target_toolkit in self.archive:
            data = self.archive[self.target_toolkit]
            self.results.toolkit = self._record_toolkit(data)
            success = True
        else:
            data = ERROR.COULD_NOT_RESOLVE.TOOLKIT.format(self.target_toolkit)
            self.results.error = data
        return success, data

    def _claim_clone(self):
        success = False
        data = None
        toolkit_resolved, toolkit = self._claim_toolkit()
        if toolkit_resolved:
            if self.target_clone in toolkit:
                data = toolkit[self.target_clone]
                self.results.clone = self._record_clone(data)
                success = True
            else:
                data = ERROR.COULD_NOT_RESOLVE.CLONE.format(self.target_clone, toolkit.name)
                self.results.error = data
        else:
            data = toolkit
        return success, data, toolkit


    def _handle_all(self):
        self.log_error("No target specified")

    def _handle_clone(self):
        self.log_kvp(KEY.RESULTS.TOOLKIT, None)
        self.log_kvp(KEY.RESULTS.CLONE, None)

    def _handle_toolkit(self):
        self.log_kvp(KEY.RESULTS.TOOLKIT, None)

    @staticmethod
    def _record_toolkits(archive):
        toolkits = []
        for toolkit in archive.toolkits:
            toolkits.append(WoodchipperToolkitHandler._record_toolkit(toolkit))
        return toolkits

    @staticmethod
    def _record_toolkit(tk, extra=None):
        toolkit_ns = WCNamespace(KEY.RESULTS.TOOLKIT)
        toolkit_ns.add(KEY.TOOLKIT.NAME, tk.name)
        toolkit_ns.add(KEY.TOOLKIT.PATH, tk.path)
        toolkit_ns.add(KEY.TOOLKIT.VERSION, tk.current.version)
        toolkit_ns.add(KEY.TOOLKIT.STATE, tk.state)
        toolkit_ns.add(KEY.TOOLKIT.CLONES, len(tk.clones))
        if extra:
            for key, value in extra:
                toolkit_ns.add(key, value)
        return toolkit_ns

    @staticmethod
    def _record_clones(toolkit):
        clones = []
        for clone in toolkit.clones:
            clones.append(WoodchipperToolkitHandler._record_clone(clone))
        return clones

    @staticmethod
    def _record_clone(clone, extra=None):
        clone_ns = WCNamespace(KEY.RESULTS.CLONE)
        clone_ns.add(KEY.CLONE.NAME, clone.name)
        clone_ns.add(KEY.CLONE.PATH, clone.path)
        clone_ns.add(KEY.CLONE.VERSION, clone.archive.version)
        clone_ns.add(KEY.CLONE.STATE, clone.state)
        if extra:
            for key, value in extra:
                clone_ns.add(key, value)
        return clone_ns



class WoodchipperHandlerAdd(WoodchipperToolkitHandler):
    def __init__(self, request, response):
        WoodchipperToolkitHandler.__init__(self, request, response, handler=HANDLER.ADD)
    def _handle_toolkit(self):
        self.results.handler = HANDLER.ADD.TOOLKIT
        WoodchipperToolkitHandler._handle_toolkit(self)
        if self.target_toolkit in self.archive:
            tk = self.archive[self.target_toolkit]
            self.log_error(ERROR.ADD.TOOLKIT.ALREADY_REGISTERED.format(tk.name, tk.path))
        elif pathlib.Path(self.request.path).is_dir():
            self.log_error(ERROR.ADD.TOOLKIT.IS_DIRECTORY.format(self.target_toolkit, self.request.path))
        else:
            self.archive.add_toolkit(self.target_toolkit, self.request.path.resolve())
            self.archive.save()
            self.results.toolkit = self._record_toolkit(self.archive[self.target_toolkit])
            self.log_success()

    def _handle_clone(self):
        self.log_kvp(KEY.CLONE.EXISTED, True)
        self.results.handler = HANDLER.ADD.CLONE
        WoodchipperToolkitHandler._handle_clone(self)
        if not self.target_toolkit in self.archive:
            self.log_error(ERROR.ADD.CLONE.INVALID_TOOLKIT.format(self.target_toolkit))
        elif self.target_clone in self.archive[self.target_toolkit]:
            cl = self.archive[self.target_toolkit][self.target_clone]
            self.log_error(ERROR.ADD.CLONE.ALREADY_REGISTERED.format(cl.name, cl.path))
        else:
            tk = self.archive[self.target_toolkit]
            target_path = pathlib.Path(self.request.path)
            descendant_path = target_path / pathlib.Path(tk.path).name
            target_is_directory = target_path.is_dir()
            if target_is_directory and descendant_path.exists():
                self.log_error(ERROR.ADD.CLONE.ALREADY_EXISTS.format(descendant_path))
            else:
                if target_is_directory:
                    target_path = descendant_path
                    shutil.copy2(tk.path, str(descendant_path))
                    self.results.existed = False
                tk.add_clone(self.target_clone, str(target_path))
                self.archive.save()
                self.results.toolkit = self._record_toolkit(tk)
                self.results.clone = self._record_clone(tk[self.target_clone])
                self.log_success()

class WoodchipperHandlerPush(WoodchipperToolkitHandler):
    def __init__(self, request, response):
        WoodchipperToolkitHandler.__init__(self, request, response, handler=HANDLER.PUSH)
    def _handle_toolkit(self):
        self.results.handler = HANDLER.PUSH.TOOLKIT
        WoodchipperToolkitHandler._handle_toolkit(self)
        toolkit_resolved, toolkit = self._claim_toolkit()
        if toolkit_resolved:
            if len(toolkit.clones) == 0:
                self.log_error(ERROR.PUSH.TOOLKIT.NO_CLONES.format(toolkit.name))
            else:
                clones = []
                for clone in toolkit.clones:
                    clones.append(self._push_clone(toolkit, clone))
                self.log_kvp(KEY.TOOLKIT.CLONES, clones)
                self.log_success()

    def _handle_clone(self):
        self.results.handler = HANDLER.PUSH.CLONE
        WoodchipperToolkitHandler._handle_clone(self)
        clone_resolved, clone, toolkit = self._claim_clone()
        if clone_resolved:
            self.results.clone = self._push_clone(toolkit, clone)
            self.results.success = self.results.clone.replaced
            self.results.error = self.results.clone.error

    def _push_clone(self, toolkit, clone):
        error = None
        replaced = False
        old_version = clone.archive.version
        if toolkit.state != STATE.UP_TO_DATE and not self.request.force:
            error = ERROR.PUSH.CLONE.TOOLKIT_NOT_PUSHABLE.format(toolkit.name)
        elif clone.state != STATE.BEHIND_CORE and not self.request.force:
            error = ERROR.PUSH.CLONE.UP_TO_DATE.format(toolkit.name, clone.name, clr_state(clone.state))
        else:
            shutil.copy2(toolkit.path, clone.path)
            clone.update()
            replaced = True
        return self._record_clone(clone, [
            (KEY.CLONE.REPLACED, replaced),
            (KEY.CLONE.OLD_VERSION, old_version),
            (KEY.CLONE.ERROR, error)])

class WoodchipperHandlerGrab(WoodchipperToolkitHandler):
    def __init__(self, request, response):
        WoodchipperToolkitHandler.__init__(self, request, response, HANDLER.GRAB)
    def _handle_toolkit(self):
        WoodchipperToolkitHandler._handle_toolkit(self)
        toolkit_resolved, toolkit = self._claim_toolkit()
        self.results.handler = HANDLER.GRAB.TOOLKIT
        if toolkit_resolved:
            if not self.request.force and toolkit.state == STATE.UP_TO_DATE:
                self.log_error(ERROR.GRAB.TOOLKIT.NO_CHANGES.format(toolkit.name))
            else:
                old_version = toolkit.archive.version
                new_version = self._increment_version(old_version)
                toolkit.set_version(new_version)
                self.results.toolkit = self._record_toolkit(toolkit, [(KEY.TOOLKIT.OLD_VERSION, old_version)])
                self.results.clones = self._record_clones(toolkit)
                self.log_success()

    @staticmethod
    def _increment_version(old_version):
        old_version_split = old_version.split('.')
        core_version_str = ".".join(old_version_split[:-1])
        old_final_tag_str = old_version_split[-1]
        old_final_tag = int(old_final_tag_str)
        new_final_tag = old_final_tag+1
        new_final_tag_str = str(new_final_tag).zfill(len(old_final_tag_str))
        # special case: o.o.9 to be updated to 0.0.10
        # - this case breaks our version comparison
        # To fix: new version = 0.0.90, append a 0
        if old_final_tag_str > new_final_tag_str:
            new_final_tag_str = old_final_tag_str + '0'
        return core_version_str+'.'+new_final_tag_str

    def _handle_clone(self):
        self.results.handler = HANDLER.GRAB.CLONE
        WoodchipperToolkitHandler._handle_clone(self)
        clone_resolved, clone, toolkit = self._claim_clone()
        if clone_resolved:
            if not toolkit.state == STATE.UP_TO_DATE and not self.request.force:
                # check for force or toolkit is up_to_date : ERROR.GRAB.CLONE.TOOLKIT_CHANGES
                self.log_error(ERROR.GRAB.CLONE.TOOLKIT_HAS_CHANGES.format(toolkit.name))
            elif not clone.state == STATE.AFTER_CORE and not self.request.force:
                # check for force or clone is after_core : ERROR.GRAB.CLONE.NO_NEW_VERSION
                self.log_error(ERROR.GRAB.CLONE.NO_NEW_VERSION.format(toolkit.name, clone.name))
            else:
                shutil.copy2(clone.path, toolkit.path)
                self.log_success()

class WoodchipperHandlerShow(WoodchipperToolkitHandler):
    def __init__(self, request, archive):
        WoodchipperToolkitHandler.__init__(self, request, archive, HANDLER.SHOW)
    def _handle_all(self):
        self.results.add(KEY.RESULTS.TOOLKITS, WoodchipperToolkitHandler._record_toolkits(self.archive))
        self.log_success()

    def _handle_toolkit(self):
        self.results.handler = HANDLER.SHOW.TOOLKIT
        WoodchipperToolkitHandler._handle_toolkit(self)
        toolkit_resolved, toolkit = self._claim_toolkit()
        if toolkit_resolved:
            self.results.add(KEY.RESULTS.CLONES, self._record_clones(toolkit))
            self.log_success()

    def _handle_clone(self):
        self.results.handler = HANDLER.SHOW.CLONE
        WoodchipperToolkitHandler._handle_clone(self)
        clone_resolved, clone, toolkit = self._claim_clone()
        if clone_resolved:
            try:
                has_changes, diff_lines = WCDiff.get_diff_from_file_paths(self.results.toolkit.path,self.results.clone.path, True)
                if not has_changes:
                    diff_lines = None
                self.results.add(KEY.CLONE.DIFF,diff_lines)
                self.log_success()
            except Exception as e:
                self.log_error(ERROR.SHOW.CLONE.UNSUCCESSFUL_DIFF)