from core.wctk_record import WCRecord
from utilities.wcutil import WoodChipperFile


class WCTracker:

    class Status:
        ERROR = -1
        SHELL = 0
        ARCHIVE = 1
        UPDATE = 2
        READY = 3

    def __init__(self, name="None", path="None", delimiter=";"):
        self.name = name
        self.path = path
        self.delimiter = delimiter
        self.status = WCTracker.Status.SHELL
        self.requires_write = False
        self.archive = None
        self.current = None

    def parse_archive(self, text):
        archive_data = text[:-1].split(self.delimiter)
        self.name = archive_data[0]
        self.path = archive_data[1]
        self.archive = WCRecord(archive_data[2], float(archive_data[3]))
        if len(archive_data) > 4:
            return archive_data[4:]
        return []

    def write_archive(self):
        return f"{self.name}{self.delimiter}{self.path}{self.delimiter}{self.archive.version}{self.delimiter}{self.archive.last_modified}"

    def read_from_archive(self, text):
        if self.parse_archive(text):
            self._set_status(WCTracker.Status.ARCHIVE)
        else:
            self._set_status(WCTracker.Status.ERROR)

    def _set_archive(self, archive):
        if not self.archive or not archive.is_equal_to(self.archive):
            self.archive = archive
            self.requires_write = True


    def update(self):
        if not self.path == "None" and not self.status == WCTracker.Status.ERROR:
            current_record = WCRecord()
            wc_file = WoodChipperFile(self.path, False)
            wc_file.read()
            # Grab last_modified
            current_record.set_datetime_as_last_modified(wc_file.last_modified())
            # Grab version
            current_record.version = wc_file.find_tag("version: ")
            self.current = current_record
            if (not self.archive) or self.current.is_higher_version_than(self.archive):
                self._set_archive(self.current)
            self._set_status(WCTracker.Status.UPDATE)
            return True
        else:
            return False

    def _set_status(self, status):
        new_status = status
        new_is_update = new_status == WCTracker.Status.UPDATE
        old_is_archive = self.status == WCTracker.Status.ARCHIVE
        is_ready = new_is_update and old_is_archive
        if is_ready:
            new_status = WCTracker.Status.READY
        self.status = new_status

    def set_version(self, new_version):
        wc_file = WoodChipperFile(self.path, False)
        wc_file.read()
        # Grab version
        wc_file.replace_tag("version: ", new_version)
        wc_file.write()
        self.update()

    def has_local_changes(self):
        if self.current.has_same_version_as(self.archive):
            return self.current.has_newer_modifications_than(self.archive)
        return False