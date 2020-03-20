#Automation of inter-rater reliability (IRR) - Markdown for "IrrKrippendorff.py"

Candice Moore
18th October 2019

This is an Python Markdown document to provide instructions for how to run IrrKrippendorff.py to automate the process of parsing pairs of JSON files to compare annotations for two annotators, and calculate Krippendorff's alpha. The script can be used when double coding, to indicate the reliability of each entity within a codeset for a group of papers. It also indicates the overall reliability of the codeset for the group of papers.

In summary, this script
- compares the codesets in the input JSON files to indicate any discrepancies (output - fileComparison.txt)
- takes pairs of JSON files and generates an excel file showing exact annotations for each annotator side by side, for each entity, and each paper (output - IrrSpreadsheetText.csv)
- generates a similar excel file giving a binary value for each entity in each paper, for each annotator, to indicate whether the entity was used or not (output - IrrSpreadsheetBinary.csv)
- calculates Krippendorff's alpha for each entity used by at least one annotator, across all papers, based on whether the entity was present in the paper or not (output values - AllPapers.csv)
- calculates an overall Krippendorff's alpha from only those entities which were annotated by at least one annotator for at least one paper (output value - 'Entities with data', within AllPapers.csv)
- calculates an overall Krippendorff's alpha for all codes, including those that were not coded by either reviewer for any paper (output value - 'All Entities', within AllPapers.csv)

This script uses a python implementation of Krippendorffs alpha (https://pypi.org/project/krippendorff/).

This work is part of the Human Behaviour Change Project (www.humanbehaviourchange.org). More information about the methods used to develop this script is currently in preparation. 

###Inputs

This script takes pairs of JSON files generated from EPPI reviewer as it's input. Each JSON file should contain data extracted by one annotator for a group of papers on EPPI reviewer.

The data used in this example is a set of JSON files exported from EPPI reviewer from data annotated as part of the human behaviour change project.

###Requirements for the script

Input files
- must be JSON files. Current version requires JSON files exported from EPPI reviewer but can be extended to other inputs
- all JSON files must be generated from the exact same codeset
- for each entity, attribute names across JSON files should be identical (including capital letters/spaces/symbols)
- within each JSON file, each codename should be unique
- for each pair of JSON files being compared, the group of papers should be identical
- commmas should be avoided in arm names and entity names as this can interfere with the script

###Step 1 - Getting set up

The first step is to save 'IrrKrippendorff.py' and your JSON files to the same folder. You will also need to install the required packages. Install pip following the instructions here (https://pip.pypa.io/en/stable/installing/). Then type "pip install krippendorff" into the command line.

###Step 2 - Inputting your files

The next step is to update the script with the names of your files saved in the same directory as the 'IrrKrippendorff.py' script. Each coder can have multiple JSON files, but they should all use the same codeset. The order in which the filenames are entered is important - for each coder, the filenames in the same position must  form a  pair i.e. they have been produced from the same group of papers. You can also rename the results file. The results file will contain Krippendorff's alpha for each entity, and for all entities taken together. To do this, you will need to edit the code on lines 14 and 15 of the script.

```python
coder1JSON = ['Behaviour1_Coder1.json','Behaviour2_Coder1.json']
coder2JSON = ['Behaviour1_Coder2.json','Behaviour2_Coder2.json']
resultsFileName = 'AllPapers.csv'
```

###Step 3 - run the script!

Once you have installed the required packages and specified your input files which are stored in the correct folder, you are ready to run the script.

Some things to note when running the script:

- Check the text printed when you  run the script. If you have a mismatch between codesets, your script will print 'It is False that the codenames are the same'. This means your inputted files don't meet the requirements and you are highly likely to come across errors
- if you receive a 'key error', it is likely that there is a mismatch between the codesets
- it is a good idea to check the fileComparison.txt output file once you've run your script, just to check that there are no issues with the codeset. The codenames should match, and there should be no duplicate codenames within JSON files
- if you are running multiple pairs of JSON files through the script and receiving a key error, you may wish to do a more thorough check to see whether there are any discrepancies between the codesets. The script compares codesets from two JSON files, so if you are entering multiple JSON files into the script, you will need to edit the script manually to run your chosen pairwise comparisons to check for discrepancies. To change the files being compared, go to line 402 of the script and edit the numbers within the square brackets (note, within the square brackets to refer to the first JSON in the list, enter 0, to refer to the second, enter 1 etc).
- the default code is to compare the first JSON for coder one to the first JSON for coder two.  The default code in the script is:

```python
if len(coder1JSON) > 1:
    codeFileReview1 = coder1JSON[0]
    codeFileReview2 = coder2JSON[0]
```

- e.g. to compare the first JSON for coder one to the second JSON for coder two you will need to change the default code to:

```python
if len(coder1JSON) > 1:
    codeFileReview1 = coder1JSON[0]
    codeFileReview2 = coder2JSON[1]
```

- e.g. to compare the second JSON for coder one to the third JSON for coder two, change the code to:

```python
if len(coder1JSON) > 1:
    codeFileReview1 = coder1JSON[1]
    codeFileReview2 = coder2JSON[2]
```

###Step 4 - check the output files

fileComparison.txt
- this text file indicates whether there are any differences between the codesets of the JSON files
- the script will only work properly if the codesets are the same, so if there are any differences, you may need to make some changes to the JSON or create a new one before running the file through the script

IrrSpreadsheetText.csv  
- this csv file contains a row for every entity within each arm in each paper, for each coder
- 'nothing coded' indicates that the entity was not coded
- 'code ticked with no value' indicates that the entity was ticked as present but no text was highlighted/given as context
- any other cells show what was highlighted for that entity
   - where there are multiple highlights for a given entity, each highlight is separated with a ";]"
   - some symbols, e.g. commas, have been replaced to preserve csv encoding
 
IrrSpreadsheetBinary.csv
- this csv file contains a row for every entity within each arm in each paper, for each coder
- 0 indicates that no text was highlighted for this entity
- 1 indicated that text was highlighted 

AllPapers.csv
- this csv file contains a row for every entity coded at least once within the set of papers, with a Krippendorff's alpha value indicating reliability between the two coders for that entity
- the row labelled Entities with data contains an alpha value for reliability between the two coders, calculated only on entities that were coded at least once
- the row labelled All Entities contains an alpha value for reliability between the two coders calculated on all entities, regardless of whether they were coded or not

###If you have any questions, or any issues running the script, contact Ailbhe Finnerty (a.finnerty@ucl.ac.uk) or Candice Moore (candice.moore.11@ucl.ac.uk)