# woodchipper-git-ignore
A simple python script for quick adding .gitignore from the commandline

## Setup
Simply run gignore.py after installing python3

## Usage
gignore initially supported the following command-line interfaces:

```shell 
gignore -s: Creates the .gitignore file if necessary and adds .wcn* to it.
gignore -s python: Creates the .gitignore file if necessary and adds .wcn*, .idea, __pycache__
gignore -a [target]: Creates the .gitignore file if necessary and adds target to it.
gignore -r [target]: IF the .gitignore file exists and contains target, removes target from the file.
gignore -c: Clears the .gitignore file without deleting it, removing every line of text from it. 
```

After implementing the WCCore system, those same routes would now be written as:

```shell
gignore setup
gignore setup python
gignore add [target]
gignore remove [target]
gignore clear
```
As an aside, the WCCore system was implemented to assume that different modes of usage should be written out and flag-like arguments should be contrained to only affecting the work of modes.

## TODO:

- Implement WCCore Technique
- Make delete wildcard-aware.