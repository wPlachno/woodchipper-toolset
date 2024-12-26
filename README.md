# woodchipper-toolset

A command line python script for versioning of text-based files and keeping them normalized between different projects.

## Why Is This Necessary?

woodchipper-toolset is designed as a CLI tool for management of a single toolkit, or a collection of files, between multiple projects. 

Several companies have a single repository with multiple applications, more popularly known as a monorepo. This technique may solve the issue of a dependency for multiple projects by having them point to the expected path of the same library, which, when described as a relative path, will change very little between different clones of the repository. 

Monorepos, however, also have some significant drawbacks: they can be used by multiple teams and may need to be used and updated frequently enough to cause race issues. The tooling needed to keep monorepos stable can be complex.

While 'woodchipper', my collection of code, rarely needs to push my tooling to these upper levels of complexity, I do prefer to have each project in its own repository. 

As I program and develop 'woodchipper', I have created a toolkit, a set of code that I use throughout several projects. As I have increased the number of solutions in my codebase, the management of these core toolkit files has become a concern. 

This is the purpose of this project: a command-line tool designed to aid in the management of these toolkit files between different repositories.

## Some Terminology

To ensure stability, we need to establish some terminology:

### A `toolkit`

A file that may be used by several projects. Each toolkit will have its own version number, tracked as a line anywhere in the file that explicitly states `Version: [VERSION]`.

### Under `watch`

A toolkit under watch is a clone of the toolkit that `wctk` is aware of and monitors.

### The `core` toolkit

A copy of the toolkit that does not belong to a separate project. This version of the toolkit may be created from a preexisting version of the toolkit, but should be copied to the archive.

### The toolkit `clones`

The copies of the toolkit that are under watch. These, while under watch by `wctk`, belong to separate projects.

### The clone `identification`

The identification of a clone is a way of describing particularly which clone you are talking about by having the toolkit name, followed by the slash, followed by the clone identifier. `[TK_NAME]/[CL_NAME]`

### The `version`

A unique number assigned to a specific copy of a toolkit to represent its cumulative changes. 

The method that `wctk` suggests is the "Major.Minor.Patch" method ("1.0.3"). This method allows for fixes to increment the `Patch` number, changes to increment the `Minor` number, and api changes to affect the `Major` number.

For the correct operation of `wctk`, the version number of each file should be listed anywhere inside the text of the file explicitly with "Version: [VERSION]". The 'Version' tag must have only the 'V' capitalized and be immediately followed by a colon. If the version tag could not be found within the file, then the version will be recorded as '-1'. 

## The Goal

With the purpose of getting the management of these files laid out, there are key use cases that need to be considered:

- Displaying all toolkits maintained by `wctk`.
- Adding a new toolkit to be watched, either from preexisting
  files, or as an empty toolkit directory that we can add to 
  later.
- Adding clones of the toolkit to be watched, whether they 
  need to be copied over, or have a preexisting copy.
- Being able to see which clones are up to date, which have a
  previous version, and which have local changes that may be 
  worth promoting to the core toolkit.
- Automatic push of changes from the core to the clones.

As an aside, there are also some 'nice-to-have' use cases:

- Automatic git pushes of toolkit updates.
- A diff production between the local clones and the core.

## The Interface

woodchipper-toolset should have the following API routes:

- `wctk`

- `wctk [target]`

- `wctk add [target] [path]`

- `wctk push [-f] [target]`

- `wctk grab [-f] [target]`

- `wctk`:
  Just running the program with no arguments will assume the mode is 'show'. With no target, the show mode will liast all of the toolkits that are being watched and their current version number.

- `wctk [TK_NAME]`:
  Only supplying a toolkit name should assume the show mode and display the information regarding only that toolkit: which clones are being watched, which version each of the clones currently has, and whether local changes exist. If there is no toolkit that matches the name, fallback to displaying all of the toolkits.

- `wctk [TK_NAME]/[CL_NAME]`:
  Supplying the toolkit name and the name of a clone should display the information regarding that clone. If the clone referred to does not exist, just list all of the clones known and their current statuses. If the toolkit does not exist, list all of the toolkits.

- `wctk add [TK_NAME] [TK_PATH]`:
  The add mode should allow for additions to the system. In this case, we should start watching the toolkit at the path and refer to it using the supplied name. If the path refers to a directory, warn the user that directories cannot be tracked and cancel out. Note that the restrictions on the names of toolkits and clones are a length of 32 characters that cannot be \, /, |, ~, ", ', `

- `wctk add [TK_NAME]/[CL_NAME] [opt:CL_PATH]`:
  This route will add a clone to the given toolkit with the given name and path. The clone path defaults to the working directory. If the clone path is a directory, look for a file in the directory whose name matches the toolkit file name, and set the clones path to that specific file. If the file pointed to by clone path at this point, copy it from the archive. If the toolkit name does not match a tracked toolkit, warn the user and cancel out.

- `wctk push [TK_NAME]`:
  The `-p`, or 'push' flag, means to copy the core to each of the clones that need it. Pushing a toolkit will overwrite any clones which have an older version of the toolkit with the core. If there are local changes, warn the user and skip that clone. If the given toolkit does not exist, warn the user and cancel out.

- `wctk push -f [TK_NAME]`:
  The `-f`, or 'force', flag means to ignore whether the clones have any local changes and overwrite them anyway. Force pushing a toolkit will copy the toolkit even if there are local changes.

- `wctk push [TK_NAME]/[CL_NAME]`:
  Pushing the clone of a toolkit will copy the toolkit to that clone unless there are local changes. If the clone does not exist, warn and fail. Do similar if the toolkit cannot be resolved.

- `wctk push -f [TK_NAME]/[CL_NAME]`:
  Force push the toolkit to the clone, overwriting any local changes with the current version of the core toolkit.

- `wctk grab [TK_NAME]/[CL_NAME]`:
  The 'grab' mode does the opposite of pushing. If you 'grab' a clone, you are copying the version of the toolkit from that clone up to the core, making the copy of the kit in that clone the new core version. A grab will only be successful if the clone's version is greater than the core.

- `wctk grab -f [TK_NAME]/[CL_NAME]`:
  When we grab with the `force` tag, we copy the clone to the core, regardless of the state of the core toolkit. 

## Structure

In order to accomplish all of these goals, we should consider the appropriate classes and their intended use.

### General Structure

As all of our intended use cases utilize the command-line, we should prepare a translation object, `WoodchipperTranslator`, whose sole purpose is to decipher the command line arguments into a `process_request`, or a group of data representing the data transactions requested by the user. 

We will use a file called `/home/.wctk_Archive.txt` to save information regarding the toolkit management between transactions. This information should include the names, paths, versions, and last_modifed_date of the core toolkits and each of their clones. This will be used to instantiate `tkManager`, a `WoodchipperToolkitManager` object and the core handler of our transactions. We will pass the `process_request` to the `tkManager`, which will use smaller classes, such as `WoodchipperToolkit` and `WoodchipperToolkitClone`, to complete the transactions. 

Once completed, `tkManager` should return a `process_summary`, a bundle of data to provide the result of the process, including whether it was successful and any significant changes made.

The `process_summary` is given to the `WoodchipperCLI`, which prints the data to the command line for the user. At this point, any modifications made to the toolkits should be noted in the archive file, saved, and we should end our process.

### The Models

With `WoodchipperToolkitManager` as the overall functional administrator, we also use `WoodchipperToolkit` and `WoodchipperToolkitClone`. 

#### WoodchipperToolkit

`WoodchipperToolkit` is the model for using and working with each individual toolkit. This is the class that contains the toolkit name, path, last_modified date, and latest version.

Toolkits will have both a `state` and a `status` - the status of a toolkit describes the loading of the information into the model, while the state refers to whether the toolkit has changes that should be saved into a new version. 

When instantiated, we pass it the toolkit name and the path, and set `status` to `initialized` and `state` to `unknown`. 

If pulling from the archive, we then give it the toolkits version and that version's timestamp. We also pass it any known clone information, allowing it to do the task of initializing the `WoodchipperToolkitClone` object for the transaction.

The `update_toolkit()` method interacts with the filesystem to get the current last_modified and the current version number, then sets the `status` to `ready` and the `state` to `up_to_date`. If the current version is higher than the version number pulled from the archive, then we drop in the new version and timestamp and do not edit the state. If the version is the same, but the timestamp is newer, than we will set the state to `has_local_changes`. Note that if the version number has not changed, we do not replace the timestamp. 

For serialization we convert the `WoodchipperToolkit` to '[NAME]|[PATH]|[VERSION]|[TIMESTAMP]|[INFO_CLONE_1]|[INFO_CLONE_2]|...|[INFO_CLONE_LAST]\n'

#### WoodchipperToolkitClone

`WoodchipperToolkitClone` is the data model for a clone of a toolkit, including the name, the path, the version, the last_modified, and its own set of state and status variables. 

Clones will be initialized by the toolkit from the archive. The data that needs to be stored into the archive consists of the name, the path, the last known version number and the timestamp of that version. When initialized, the status will be set to `initialized` and the `state` will be set to `unknown`. 

`update_clone()` is a `WoodchipperToolkitClone` method that queries the filesystem for the important information that we care about regarding the clone, including the current version, and the last_modified date, and sets the `status` to `ready` and the `state` to `behind_core`. 

If the version number from update is newer than the archive, we simply update the `WoodchipperToolkitClone` version number and the current timestamp. 

If both the version number and the timestamp match the core toolkit, than update the `state` to `up_to_date`. If it is higher or the timestamp is newer than the timestamp for the core toolkit, update `state` to `has_local_changes`. 

For serialization, we convert the `WoodchipperToolkitClone` to a string: '[NAME]~[PATH]~[VERSION]~[TIMESTAMP]'

#### Records

When considering the last_modifed_date and version, internally referred to as a record, we track three sets for each clone and each toolkit: the record listed in the archive, the current record of the file, as well as the record to be written to the archive when execution completes. 

For each toolkit, if the core file's current_record is a different version than the archive_record, then we can just immediately replace the archive_record with the current_record. If we were saving backups, than anytime the core version changes, we would save it to a backup. If the current_records last_modified_date, or lmd, is different from the archive_record, we have local changes. It would make sense to assume that we want the backup copy of a version to be the oldest lmd of that version, and that any future changes to that same version are really just changes that will become the next version. 

For each clone, if the current version is different, then we can immediately replace the archive_record with the current_record. If the lmd is different it has local_changes. 

Thus, for both, changes in version should be notated immediately, and changes in lmd signal has_local_changes

## Operation

### Listing Functionality

Many of the routes simply list the data correlating to a subset of information. 

#### All Toolkits

Listing the toolkits will list each toolkit as: '[NAME]: [VERSION] ([STATE])\n'. 

#### Specific Toolkit

When looking at individual toolkits, we start with a header describing the toolkit - 
'[NAME]: [VERSION] ([STATE])\n[PATH]\n' 

- then, list each clone with: 
  '- [NAME]: [VERSION] ([STATE])\n'. 

#### Specific Clone

If we list a specific clone, than we should have 
'[NAME]: [VERSION] ([STATE])\n[PATH]\n'. 
As of version 0.0.1.000, we will also display a diff between the core and clone.

### Addition Functionality

Some of the routes are designed for adding toolkits or clones. Note that when working with paths pased in by the user, we should assume they need to be resolved by Pathlib. When we save them to the Archive, they should be saved as a full path. 

#### Adding a Toolkit

When adding a toolkit, we create a new `WoodchipperToolkit` with the name and path given by the user, then immediately call the `update_toolkit()` method, and add it to the archive. The output should simply read 'Added new toolkit [NAME]: [VERSION].\n'. If the path could not be resolved to a single file, the output would read, '[NAME] could not be resolved to a toolkit.\n'. If the version tag cannot be found within the file, it will be logged as '-1'.

#### Adding a Clone

If the toolkit name resolves, then we allow the `WoodchipperToolkit` to instantiate a new clone using `add_clone()` method, passing in the name and path. The toolkit should then create a stub clone with the name and path. If the file does not exist, we should copy down the core toolkit to the path. Then, we call 'update_clone()' method. When done and the archive has been saved, let the user know: 'Added [TOOLKIT_NAME] clone [NAME]: [VERSION] at [PATH].\n' If the toolkit could not be resolved, print 'Could not resolve toolkit [NAME].\n', then do the full toolkit list as if the user had just typed `wctk`.

### Copying Functionality

The copying functionality is where this application becomes actually useful. There are currently two types of copying supported by the application: *Pushing* and *Grabbing*. *Pushing* refers to copying from the core down to the clones, whereas *grabbing* pulls from the clones and replaces the core. 

#### Pushing a Clone

If the toolkit and clone name correctly resolve, and the clone state is `behind_core` or the `force` tag is present, we should copy the core file down to the path of the clone, then call `update_clone()` and save the archive. If successful, we should print '[TOOLKIT_NAME]/[CLONE_NAME] successfully updated.\n', then print the info of that particular clone. If the toolkit name could not be resolved, print 'Could not find toolkit [TOOLKIT_NAME]\n', then print the full toolkit list. If the clone could not be resolved, print 'Could not find clone [CLONE_NAME].\n', then print the individual toolkit. 

#### Pushing a Toolkit

When we push a toolkit, we are essentially pushing every clone monitored for that toolkit. Essentially, we want to look at each clone of a toolkit and, if the `force` tag was included, push each clone. Without the `force` tag, only push if the clone's state is `behind_core`, and let the user know if the clone's state was 'has_local_changes' - '[CLONE_NAME] has local changes and was ignored.\n', or if the clone's state was `up_to_date` - '[CLONE_NAME] already up to date.\n'.

#### Grabbing a Clone

When we grab a clone, our goal is to copy a new version of the toolkit to replace the core. If the toolkit or clone could not be resolved, warn the user as we have described for previous functionality. If the clone's version is higher than the core or the `force` tag was included, we should copy the file from the clone path to the core toolkit path. Then, print 'Grabbed [CLONE_NAME].\nCore now at version [VERSION].\n'.

#### Grabbing a Toolkit

When we use the grab on a toolkit, we save any local changes as a new version.

#### Configuration

There are a couple of app-wide variables that we may need to adjust. This includes `archive-path`, the destination of the archive where we keep copies of the toolkits, and `debug`, a boolean representing whether or not we should print debug statements.

## To-Do

- Formatting
  - Order imports
    - sys
    - utilities
    - interface
    - core
- Refactoring
  - Separate constants into package specific constants files.
  - Separate out WCCore Error Handling. 
- Functionality
  - Mode to list current directory with wctk details
  - Better Help messages.
    - Headers should be colored (blue?)
    - Extra line between usage and description
  - Add modes for:
    - Remove Toolkit
    - Edit Toolkit
  - Auto-detection when clone moved?
  - Alter tag detection so that Version does not require colon.

## Versions

### 0.0.1.001

- Integrated the WoodchipperCore system.
- Added:
  - core.wctk_handlers.py
  - interface.wctk_printer.py
  - utilities.wccli.py
  - utilities.wccontroller.py
  - utilities.wcmodehandler.py
  - utilities.wcmodeprinter.py
  - utilities.wcprinter.py
  - utilities.wcresponse.py
- Removed:
  - wctk_cli.py
  - wctk_controller.py
  - wctk_handler.py

### 0.0.1.000

- Feature complete, but grab and push need more testing.

- Added:
  
  - wctk.py - The core command-line script
  - constants.py - Constants for the wctk scripts
  - wctk_cli.py - The command line interface controller
  - wctk_request.py - The cli parser for this script
  - wcparser.py - WoodchipperParser, a simple ArgParse replacement
  - test_parser.py - Tests for correct command-line interpretation
  - wctk_printer.py - A simple, wcprofile-aware printing module.
  - wctk_controller.py - The controller between the cli and the data models
  - wctk_handler.py - The event handlers created by the controller to work on the models
  - wctk_archive.py - A collection of toolkits
  - wctk_toolkit.py - The toolkit model
  - wctk_clone.py - The clone model
  - wctk_tracker.py - A base model for tracking a name, a path, and a record
  - wctk_record.py - A model of the version and the last modified date
  - wctk_diff.py - Compiles a diff between two files.

- Functionality Added:
  - Command line parsing, including wcprofile configuration.
  - 'Show' functionality
    - Show Clone now also prints out diff of core -> clone
  - 'Add' functionality
  - 'Push' functionality
  - 'Grab' functionality
    - Grab Toolkit now increases the version of the toolkit appropriately. 
      
### 0.0.0.1

- Added wcutil and wcconstants