# woodchipper-templates
A script for taking a file and using simple language to excise text to new files.
Written by: William Plachno

## Overview 

### Problem:
Many times, when inputting data into my personal markdown library, I find myself with a file that has text that should be removed to another file. For example, when inserting a table for a ttrpg, I might have a file that references the table and describes every possibility, sometimes each possibility having several different kinds of information. In this example, we would want to be able to split this file by moving out the table to a file, then each possibility into their own sets of files.

### Solution:
If we could add some special text to the file as control tokens, we can run a script, wctmp.py, to parse the tokens and do the appropriate text replacement and file creation. 

## Implementation

### Control Tokens
Our control tokens will take the form of two sets of grouping characters. The first, `@{ADDRESS|TEXT}`, will hold the relative address of the file to be moved to, then any replacement text, separated by a '|'. The second grouping takes the form of `{{TEXT_OF_FILE}}`, simply a container for what should be moved to the new file. Altogether, we get a single element, `@{ADDRESS|TEXT}{{TEXT_OF_FILE}}`.
The information within the control tokens should be as easy-to-use as possible. The address should be relative *or* absolute. The text should have the ability to be parsed for control tokens.
For ease of communication, we will give these sequences names: `start_sequence` is '@{', `delimiter` is '|', `text_trigger` is '}{{', and `end_sequence` is '}}'. 

### Interface
Using Python, we can easily generate a basic CLI: 'py wctmp.py table.md', the script call with a single control file. The target file should be the file with the control tokens. Our interface should eventually allow a list of control files. 
The output should be relatively simple, configurable with a verbosity flag. 0 means no output, 1 means just `success`/`fail`, 2 should include the file names, and 3 should print out all files involved. 
There should also be a command line flag, `debug`, for marking that no files should be created or modified, for debugging the users control files.

### Text Classes
We will need to have a parent class, `WoodchipperTemplatingFile`, which should have a `file_path`, and a `file_content`, and have a method `save` to create a file at the path with the content, overwriting any file that exists there. `WoodchipperControlFile` will derive from this class, but overwrite the `save` method to just use whatever construct we used to read in the text for parsing. The `WoodchipperTokenFile` class will also derive from `WoodchipperTemplatingFile`, but also hold a string `replacement_text`.

### The Parse
For each control file, we should open the file and read the text. We will have a stack `file_stack` on which we will be placing `WoodchipperTemplatingFile` objects. The first on the stack should be the `WoodchipperControlFile`. We will search through the text, waiting to find `start_sequence`. As soon as we find one, we find the first `text_trigger` and enter all the data between them into a `WoodchipperTokenFile` and add it to `file_stack`. Whenever we hit an `end_sequence`, we pop the last WCTF from `file_stack`, add the intermediary text as `file_content`, and add the WCTF to a `file_list` array. When this happens, we should also add the popped WCTF object's replacement text to the text of the now-top WCTF on the `file_stack`. 
Once we reach the end of the file text, we add the `WoodchipperControlFile` to `file_list`. Then we save each WCTF in `file_list` and output as necessary.

## Future Plans

### Multiple Paths
Our first run at the program will accept only one control file path from the CL each run. In order to support multiple paths from one call, `wcparser` will need to be modified to allow for 'bucket' arguments, arguments that provide an array of some sort, whether it be a specific number, or any positional arguments past that point.

### Force Argument
There may be times that we simply want to overwrite the files as we go. In our first write of this script, that will be safeguarded, not allowing a complete file creation if a non-control file exists. We should add a `-f` flag to force the program to proceed with the file overwrites. 