# Test Control File

This file is intended to serve as a control file for testing the Woodchipper Templating script. 

## Things to test

1. Opening and reading a [control file.md|control file].
2. Checking that extraction leaves just the [library/replacement text.md|replacement text].
3. Checking that extraction can have no [library/replacement text.md|replacement text].
4. Extraction of text into a [library/new/relative file.md|relative file] in the same directory.
5. Extraction of text into a [library/new/relative file.md|relative file] in a different directory.
6. Extraction of text into a [library/new/relative file.md|relative file] in a new directory.
7. Extraction of text overwriting a [library/new/relative file.md|relative file]. 
8. Extraction of text to a file with an [/home/osboxes/Documents/Code/woodchipper-templates/library/absolute path.md|absolute path] in an existing directory.
9. Extraction of text to a file with an [/home/osboxes/Documents/Code/woodchipper-templates/library/absolute path.md|absolute path] in a [/home/osboxes/Documents/Code/woodchipper-templates/library/new2/non-existent directory.md|non-existent directory].

## Setup 

Before running these tests, you should set up the test environment.

### Test Computer

These tests should be run on a Linux machine with Python installed. 

### File Structure

It doesn't matter where you put the script, but this file should be put and run from `/home/osboxes/Documents/Code/woodchipper-templates/`. Within the same directory, add a directory called `library`, and put a file called `test.md` inside of it. `test.md` should only contain the text "The test has not been run." Explicitly, there should be no directories inside `library`. 

### Setup Steps

```terminal 
cd /home/osboxes/Documents/Code/woodchipper-templates/
rm -r library
mkdir library
echo The test has not been run. | library/test.md
```

## Tests

### Test 1: Opening and Reading

This test is simple. Was this file read? This is easy to see if Verbosity is set to 3.

#### Steps

1. Alias script

```terminal
alias wctmp='python3 /home/osboxes/Documents/Code/woodchipper-templates/wctmp.py'
```
2. Set debug and verbosity

```terminal
wctmp config debug on verbosity 3
```

3. Parse this file

```terminal
wctmp file_for_testing.md
```

4. Check the warning, then force execution

```terminal
wctmp file_for_testing.md -f > test.txt
```

#### Expected

- After step 3, the script should return an error, describing that a file could be overwritten by the extraction process.
- The script should run successfully. 
- `test.txt` should list every file that would have been created by the script. 
  - Since we turned on `debug` (in 1:2, test 1:step 2), no files will have been completed yet.   

### Test 2: Replacement Text

Is the replacement text below? Note that this is also a test to make sure our script handles a token with no actual file extraction.

@{|Here is some replacement text.}{{}}

#### Expected

- In the proposed version of `file_for_testing.md`, line 71 should have no text. 
  - In fact, lines 70-72 should all be empty, leaving an awkward gap between the test 2 description and the `Expected` header.

### Test 3: No Replacement Text

Make sure that there is only one empty line between this line and the `expected` header. Also notice that this covers testing for an empty token.
#{}{{}}
#### Expected

- Line 80 of the proposed `file_for_testing.md` should have no text. 
  - There should be no text between the Test 3 description and the `Expected` header.  

### Test 4: Same-Folder Extraction

This test should extract the text of [control file.md|#{control file.md|control file}{{
A control file is a file that includes tokens for controlling the Woodchipper Templating system. 
Tokens can be inserted anywhere in a file. They take the shape of "\@\{file_path|[library/replacement text.md|replacement_text]}{\{file_text}\}" without any of the \ characters.
}}] to its rightful place as a separate file in the working directory.

#### Steps

1. Turn off debug mode.

```terminal 
wctmp config debug off
```

2. Run the script 

```terminal
wctmp file_for_testing.md
```

#### Expected

- The script should run successfully. 
- `control file.md` should now exist with the following content:
> 
> A control file is a file that includes tokens for controlling the Woodchipper Templating system. 
> Tokens can be inserted anywhere in a file. They take the shape of "\@\{file_path|[library/replacement text.md|replacement_text]}{\{file_text}\}" without any of the \ characters.
>
- The test 4 description on line 98 in `file_for_testing.md` should read:
>This test should extract the text of [control file.md|control file] to its rightful place as a separate file in the working directory.

### Test 5: Different-Directory Extraction
This is line 126
For this test, we will be extracting the [library/replacement text.md|@{library/replacement text.md|replacement text}{{
Text that replaces the token when using the Woodchipper Templating script.
}}] file to `library/replacement text.md`.

#### Expected

- `library/replacement text.md` should be successfully created with the following content:

> 
> Text that replaces the token when using the Woodchipper Templating script.
> 

- Line 127 of `file_for_testing.md`, the description of Test 5, should read:

> For this test, we will be extracting the [library/replacement text.md|replacement text] file to `library/replacement text.md`.

### Test 6: New-Directory Extraction

The directory 'library/new' should be non-existent after setup of the tests. When we do the test below, it should create that directory and put the [library/new/relative file.md|relative file] markdown file inside of it.

@{library/new/relative file.md|Test Complete}{{
A relative file is simply a file defined by a file path that is relative to the current working directory. 
}}.

#### Expected

- `library/new/relative file.md` should be successfully created with the following content:

> 
> A relative file is simply a file defined by a file path that is relative to the current working directory.
> 

- The description of test 6 on line 145 of `file_for_testing.md` should read:

> Test Complete.

### Test 7: Overwriting Extraction

After setup, the library directory should have a file, `test.md`, which states "The test has not been run.". After this test @{library/test.md|has been completed}{{The test has been successfully completed.}}, it should be overwritten to reflect so.

#### Expected

- `library/test.md` should be successfully overwritten with the following content:

> The test has been successfully completed.

- Line 161 of `file_for_testing.md`, the description of Test 7, should read:

> After setup, the library directory should have a file, `test.md`, which states "The test has not been run.". After this test has been completed, it should be overwritten to reflect so.

### Test 8: Absolute Extraction

This test is to see if [/home/osboxes/Documents/Code/woodchipper-templates/library/absolute path.md|absolute paths] are @{/home/osboxes/Documents/Code/woodchipper-templates/library/absolute path.md|understood}{{
An absolute path determines a file by listing the parent directories all the way to the root of the file system.
}}.

#### Expected

- `/home/osboxes/Documents/Code/woodchipper-templates/library/absolute path.md` should now exist with the following content:

>
> An absolute path determines a file by listing the parent directories all the way to the root of the file system.
> 

- Line 175 of `file_for_testing.md`, the description of Test 8, should read:

> This test is to see if [/home/osboxes/Documents/Code/woodchipper-templates/library/absolute path.md|absolute paths] are understood.

### Test 9: Absolute Extraction to a new Directory

While we now know that absolute paths work, we need to double check that it works with [/home/osboxes/Documents/Code/woodchipper-templates/library/new2/non-existent directory.md|${/home/osboxes/Documents/Code/woodchipper-templates/library/new2/non-existent directory.md|non-existent]}{{
A non-existent directory is not yet created in the current file-structure.
}} directories.

#### Expected

- `/home/osboxes/Documents/Code/woodchipper-templates/library/new2/non-existent directory.md` should now exist with the following content:

>
> A non-existent directory is not yet created in the current file-structure.
> 

- Line 191 of `file_for_testing.md`, the description of Test 9, should read:

> While we now know that absolute paths work, we need to double check that it works with [/home/osboxes/Documents/Code/woodchipper-templates/library/new2/non-existent directory.md|non-existent] directories.

## Considerations

This test suite will test as much as possible without varying the control file. If we wrote tests to do so, we would design them to secure: 

- Control files with no tokens.
  - A control file with no tokens should be handled gracefully, simply stating that script execution completed successfully.

- Large control files
  - Stress testing machines with different size control files could provide us with some benchmarks for how complex these files can get before the script starts showing wear.

- Incorrectly formated control files
  - When the user tries to run the script on a file with inconsistent tokens, the script should notify the user, preferably with some information regarding a potential solution- perhaps whether there was an extra or missing set of `end_sequences`.