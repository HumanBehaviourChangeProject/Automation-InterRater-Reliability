########################################################################################################################
#   This script takes pairs of JSON files exported from EPPI reviewer using identical coding schemes on the same group of
#   papers. Each JSON file includes annotations for a coder. The script produces a csv file with a column per coder
#   giving the cell a value of 1 if the coder annotated the corresponding attribute for the corresponding paper, and
#   0 if the coder did not annotate the corresponding attribute for the corresponding paper. An excel file
#   showing the text annotated by each coder is also generated.
########################################################################################################################


import json
import krippendorff
import csv

coder1JSON = ['Behaviour1_Coder1.json', 'Behaviour2_Coder1.json']
coder2JSON = ['Behaviour1_Coder2.json', 'Behaviour2_Coder2.json']
resultsFileName = 'IRR_Results.csv'

#   the getCodeSet function parses the json file and returns a list where the first element is a list of codeIDs, and
#   the second element is a list containing a list for each attribute where the first element is the attributeID and
#   the second is the attribute name

def getCodeSet(jsonFileName):

    with open(jsonFileName, encoding="utf8") as f:
        codesDict = json.load(f)

    f.close()

    del codesDict['References']

    codeSetList = []
    codeIDs = []
    codeNames = []

    def recursiveCodesParser(codeSetJsonDict):

        for attribute in codeSetJsonDict['Attributes']['AttributesList']:

            codeSetList.append([attribute['AttributeId'], attribute['AttributeName'].replace(',', ';;;;')])
            codeIDs.append(attribute['AttributeId'])
            codeNames.append(attribute['AttributeName'].replace(',', ';;;;'))

            if 'Attributes' in attribute:

                recursiveCodesParser(attribute)

        return [codeIDs, codeSetList, codeNames]

    codeSetList = recursiveCodesParser(codesDict['CodeSets'][0])

    return codeSetList

#   the getPapersForCoderJson function reads the JSON file and creates a list of lists where the first list is a list of
#   paper IDs and the second is a list containing a pair for each paper where the first is the paper ID and the second
#   is the short title

def getPapersFromCoderJson(jsonFileName):

    with open(jsonFileName, encoding="utf8") as f:
        papersData = json.load(f)
        f.close()

    del papersData['CodeSets']

    listOfPapers = []
    paperIDs = []
    paperNames = []

    for paper in papersData['References']:

        listOfPapers.append([paper['ItemId'], paper['ShortTitle']])
        paperIDs.append(paper['ItemId'])
        paperNames.append(paper['ShortTitle'])

    return [paperIDs, listOfPapers, paperNames]

# getCodenamesDiscrepancies compares the codesets to give the entities present in one codeset but not in the other and vice versa. It also checks
# whether there are any duplicate attribute names within the codesets

def getCodenameDiscrepancies(codenamesForReview1, codenamesForReview2, review1IDs, review2IDs):

    namesInReviewNotReview2 = []
    namesInReview2NotReview1 = []
    loopReview1Codename = []
    loopReview2Codename = []
    loopReview1CodeID = []
    loopReview2CodeID = []
    nameDuplicatesReview1 = []
    nameDuplicatesReview2 = []
    IDDuplicatesReview1 = []
    IDDuplicatesReview2 = []
    IDsInReview1NotReview2 = []
    IDsInReview2NotReview1 = []


    for i in range(len(codenamesForReview1)):
        review1IDs[i] = str(review1IDs[i])

    for i in range(len(codenamesForReview2)):
        review2IDs[i] = str(review2IDs[i])

    for i in range(len(codenamesForReview1)):

        if codenamesForReview1[i] not in codenamesForReview2:

            namesInReviewNotReview2.append(codenamesForReview1[i])

        if codenamesForReview1[i] in loopReview1Codename:

            nameDuplicatesReview1.append(codenamesForReview1[i])

        if review1IDs[i] in loopReview1CodeID:

            IDDuplicatesReview1.append(review1IDs[i])

        if review1IDs[i] not in review2IDs:

            IDsInReview1NotReview2.append(review1IDs[i])

        loopReview1Codename.append(codenamesForReview1[i])
        loopReview1CodeID.append(review1IDs[i])

    for i in range(len(codenamesForReview2)):

        if codenamesForReview2[i] not in codenamesForReview1:

            namesInReview2NotReview1.append(codenamesForReview2[i])

        if codenamesForReview2[i] in loopReview2Codename:

            nameDuplicatesReview2.append(codenamesForReview2[i])

        if review2IDs[i] in loopReview2CodeID:
            IDDuplicatesReview2.append(review2IDs[i])

        if review2IDs[i] not in review1IDs:
            IDsInReview2NotReview1.append(review2IDs[i])

        loopReview2Codename.append(codenamesForReview2[i])
        loopReview2CodeID.append(review2IDs[i])

    textFile = 'It is ' + str(review1IDs == review2IDs) + ' that the codeIDs are the same. There are ' + str(len(review1IDs)) + ' IDs for review 1 and there are ' + str(len(review2IDs)) + ' IDs for review 2 \n\n' + 'There are, ' + str((len(codenamesForReview1))) + ' codenames for review 1. There are, ' + str((len(codenamesForReview2))) + ' codenames for review 2.\n\n' + 'It is ' + str(codenamesForReview1 == codenamesForReview2) + ' that the codenames are the same. The attribute names that are in codeset 1 but not codeset 2 are: ' + ', '.join(namesInReviewNotReview2) + '\n\n' + 'The attribute names that are in codeset 2 but not in codeset 1 are: ' + ', '.join(namesInReview2NotReview1) + '\n\n' + 'The IDs that are in codeset1 but not codeset 2 are: ' + ', '.join(IDsInReview1NotReview2) + '\n\nThe IDs that are in codeset2 but not codeset 1 are: ' + ', '.join(IDsInReview2NotReview1) + '\n\n' + 'The duplicate names in codeset1 are, ' + ', '.join(nameDuplicatesReview1) + '\n\n' + 'The duplicate names in codeset2 are, ' + ', '.join(nameDuplicatesReview2) + '\n\nThe ID duplicates in codeset 1 are, ' + ', '.join(IDDuplicatesReview1) + '\n\nThe ID duplicates in codeset 2 are, ' + ', '.join(IDDuplicatesReview2)

    print("It is " + str(codenamesForReview1 == codenamesForReview2) + ' that the codenames are the same')

    return(textFile)

#The checkCodesets function runs the getCodenameDiscrepencies function on the inputed reviews and adds review name to the output text

def checkCodesets(review1File, review2File):

    overallText = ''

    review1IDs = getCodeSet(review1File)[0]
    review2IDs = getCodeSet(review2File)[0]

    review1codenames = getCodeSet(review1File)[2]
    review2codenames = getCodeSet(review2File)[2]

    newText = getCodenameDiscrepancies(review1codenames, review2codenames, review1IDs, review2IDs)

    overallText = overallText + 'Comparing ' + review1File + ' and ' + review2File + ':\n\n' + newText + '\n\n****************\n\n'

    return overallText

# the produceCsv function takes a pair of JSON files as input, parses the JSON files to extract the annotations, and produces two csv strings
# (binary and text) summarising each coders annotations for each paper, arm and attribute

def produceCsv(coder1FileName, coder2FileName):

    coder1codeset = getCodeSet(coder1FileName)[0]

    codesForSet = getCodeSet(coder1FileName)

    papersAndNames = getPapersFromCoderJson(coder1FileName)

    #   presuming the codesets are the same, the list of code IDs is set to the codeset obtained from coder1's json file.
    #   If the codesets are not identical this will cause errors or issues with the output data

    listOfCodeIDs = coder1codeset

    #   the below function parses each json file into a nested dictionary containing the text annotations for each paperID,
    #   attributeID and arm. Where there is more than one piece of text annotated for a particular attribute for a
    #   particular arm, these are appended to give one item for each attribute for each arm in a paper

    def annotationsParser(jsonFile):

        with open(jsonFile, encoding="utf8") as f:
            dataDict = json.load(f)

        f.close()

        del dataDict['CodeSets']

        coder1Dict = {}

        for nPapersDict in range(len(dataDict["References"])):   #starts looping through the papers

            currentPaper = dataDict["References"][nPapersDict]["ItemId"]  #gets ID of current paper

            coder1Dict[currentPaper] = {}

            if "Codes" in dataDict["References"][nPapersDict]:  # checks whether the paper has any codes

                listOfCodesForPaper = []

                for nCodeTicked in range(len(dataDict["References"][nPapersDict]["Codes"])):    #loops through the codes for the paper in the current loop

                    armDict = {}

                    if not dataDict["References"][nPapersDict]["Codes"][nCodeTicked]["AttributeId"] in listOfCodesForPaper: #checks whether the code has already been seen for paper

                        coder1Dict[currentPaper][
                            dataDict["References"][nPapersDict]["Codes"][nCodeTicked]["AttributeId"]] = {}  #sets up a dict structure for the coder - paper>attributeID = empty dict

                        if "ItemAttributeFullTextDetails" in dataDict["References"][nPapersDict]["Codes"][nCodeTicked]: #if code has been ticked

                            for i in range(len(dataDict["References"][nPapersDict]["Codes"][nCodeTicked]["ItemAttributeFullTextDetails"])): #loops through arms for paper>attribute

                                if i == 0:  #if it's the first arm, it creates an arm dict with the arm title and assigns value of the annotated text

                                    armDict[
                                        dataDict["References"][nPapersDict]["Codes"][nCodeTicked]["ItemAttributeFullTextDetails"][
                                            i]["ItemArm"].replace(',', ';;;;')] = \
                                    [dataDict["References"][nPapersDict]["Codes"][nCodeTicked]["ItemAttributeFullTextDetails"][i][
                                        "Text"]]

                                else:       #if it's another arm it append to an arm dict with the name, as it's always another piece of text for that attribute, for that arm
                                    armDict[
                                        dataDict["References"][nPapersDict]["Codes"][nCodeTicked][
                                            "ItemAttributeFullTextDetails"][i]["ItemArm"]].append(dataDict["References"][nPapersDict]["Codes"][nCodeTicked]["ItemAttributeFullTextDetails"][i]["Text"])


                                coder1Dict[currentPaper][dataDict["References"][nPapersDict]["Codes"][nCodeTicked]["AttributeId"]] = armDict # the arm dict is assigned to paper>attribute for the coder dict

                        else: #if there is no annotated text, the armdict>armtitle is assigned 'code ticked no value' and this is assigned to the paper>attribute>arm

                            armDict[dataDict['References'][nPapersDict]["Codes"][nCodeTicked]['ArmTitle']] = "code ticked with no value"
                            coder1Dict[currentPaper][dataDict["References"][nPapersDict]["Codes"][nCodeTicked]["AttributeId"]] = armDict


                        listOfCodesForPaper.append(dataDict["References"][nPapersDict]["Codes"][nCodeTicked]["AttributeId"]) # code not seen for paper so added to list

                    else:   #if the code has been seen for the paper

                        if "ItemAttributeFullTextDetails" in dataDict["References"][nPapersDict]["Codes"][nCodeTicked]: #if it has text coded

                            for i in range(len(dataDict["References"][nPapersDict]["Codes"][nCodeTicked]["ItemAttributeFullTextDetails"])): #as above, but must be for diff arm

                                if i == 0:

                                    coder1Dict[currentPaper][dataDict["References"][nPapersDict]["Codes"][nCodeTicked]["AttributeId"]][
                                        dataDict["References"][nPapersDict]["Codes"][nCodeTicked]["ItemAttributeFullTextDetails"][i][
                                            "ItemArm"].replace(',', ';;;;')] = \
                                    [dataDict["References"][nPapersDict]["Codes"][nCodeTicked]["ItemAttributeFullTextDetails"][i]["Text"]]

                                else:

                                    coder1Dict[currentPaper][
                                        dataDict["References"][nPapersDict]["Codes"][nCodeTicked]["AttributeId"]][
                                        dataDict["References"][nPapersDict]["Codes"][nCodeTicked][
                                            "ItemAttributeFullTextDetails"][i][
                                            "ItemArm"].replace(',', ';;;;')].append(dataDict["References"][nPapersDict]["Codes"][nCodeTicked]["ItemAttributeFullTextDetails"][i]["Text"])
                        else: #if no text coded assigned 'coder ticked with no value'
                            coder1Dict[currentPaper][dataDict["References"][nPapersDict]["Codes"][nCodeTicked]["AttributeId"]][dataDict["References"][nPapersDict]["Codes"][nCodeTicked]["ArmTitle"]] = "code ticked with no value"

        return coder1Dict

    coder1Annotations = annotationsParser(coder1FileName)
    coder2Annotations = annotationsParser(coder2FileName)
    masterAnnotationsDict = {}

    #   the below function creates a nested dictionary with a nested key for each paper, attribute and arm and coder,
    #   containing the text annotation for each coder

    for paper in coder1Annotations:

        masterAnnotationsDict[paper] = {}

        for attribute in listOfCodeIDs:

            masterAnnotationsDict[paper][attribute] = {}

            if (attribute in coder1Annotations[paper]) and (attribute in coder2Annotations[paper]):

                for arm in coder1Annotations[paper][attribute]:

                    masterAnnotationsDict[paper][attribute][arm] = {}

                    masterAnnotationsDict[paper][attribute][arm]["coder1codes"] = coder1Annotations[paper][attribute][arm]

                    if arm in coder2Annotations[paper][attribute]:

                        masterAnnotationsDict[paper][attribute][arm]["coder2codes"] = coder2Annotations[paper][attribute][arm]

                    else:

                        masterAnnotationsDict[paper][attribute][arm]["coder2codes"] = "nothing coded"

                for arm in coder2Annotations[paper][attribute]:

                    if arm not in masterAnnotationsDict[paper][attribute]:

                        masterAnnotationsDict[paper][attribute][arm] = {}

                        masterAnnotationsDict[paper][attribute][arm]['coder2codes'] = coder2Annotations[paper][attribute][arm]

                        masterAnnotationsDict[paper][attribute][arm]['coder1codes'] = "nothing coded"

            elif (attribute in coder1Annotations[paper]) and not (attribute in coder2Annotations[paper]):

                for arm in coder1Annotations[paper][attribute]:

                    masterAnnotationsDict[paper][attribute][arm] = {}

                    masterAnnotationsDict[paper][attribute][arm]['coder1codes'] = coder1Annotations[paper][attribute][arm]

                    masterAnnotationsDict[paper][attribute][arm]['coder2codes'] = "nothing coded"

            elif (attribute in coder2Annotations[paper]) and not (attribute in coder1Annotations[paper]):

                for arm in coder2Annotations[paper][attribute]:

                    masterAnnotationsDict[paper][attribute][arm] = {}

                    masterAnnotationsDict[paper][attribute][arm]['coder2codes'] = coder2Annotations[paper][attribute][arm]

                    masterAnnotationsDict[paper][attribute][arm]['coder1codes'] = "nothing coded"

            else:

                masterAnnotationsDict[paper][attribute] = "nothing coded"



    line = ""
    textLine = ""

    #   the below creates a csv string to create the desired csv table format, converting text values into 0's or 1's
    #   depending on whether any text was annotated

    for paper in papersAndNames[1]:

        for attribute in codesForSet[1]:

            if masterAnnotationsDict[paper[0]][attribute[0]] == "nothing coded":

                line = line + str(paper[0]) + ',' + paper[1] + "," + str(attribute[0]) + ',' + attribute[1] + ',' + "Whole Study" + "," '0' + ',' + '0' + "\n"
                textLine = textLine + str(paper[0]) + ',' + paper[1] + "," + str(attribute[0]) + ',' + attribute[1] + ',' + "Whole Study" + "," 'nothing coded' + ',' + 'nothing coded' + "\n"

            else:

                for arm,value in masterAnnotationsDict[paper[0]][attribute[0]].items():

                    if arm == '':

                        armName = "Whole Study"

                    else:

                        armName = arm

                    def sortCodes(individualCode):

                        if individualCode == "nothing coded":

                            outputCode = "0"
                            textOutputCode = "nothing coded"

                        elif individualCode == "code ticked with no value":

                            outputCode = "1"
                            textOutputCode = "code ticked with no value"

                        elif len(individualCode) == 1:

                            outputCode = "1"
                            textOutputCode = (((((individualCode[0].replace('\n',"")).replace(",","####*")).lstrip('Page')).replace("[¬e]","")).replace("[¬s]",""))[3:]

                        else:

                            outputCode = "1"
                            textOutputCode = ""
                            for item in individualCode:
                                textOutputCode = textOutputCode + (((((item.replace('\n', "")).replace(",", "####*")).lstrip('Page')).replace("[¬e]", "")).replace("[¬s", ""))[3:] + ";"

                        return([outputCode, textOutputCode])

                    coder1codes = sortCodes(masterAnnotationsDict[paper[0]][attribute[0]][arm]['coder1codes'])[0]
                    coder2codes = sortCodes(masterAnnotationsDict[paper[0]][attribute[0]][arm]['coder2codes'])[0]
                    coder1text = str(sortCodes(masterAnnotationsDict[paper[0]][attribute[0]][arm]['coder1codes'])[1])
                    coder2text = str(sortCodes(masterAnnotationsDict[paper[0]][attribute[0]][arm]['coder2codes'])[1])
                    line = line + str(paper[0]) + ',' + paper[1] + "," + str(attribute[0]) + ',' + attribute[1] + ',' + armName + "," + coder1codes + ',' + coder2codes + "\n"
                    textLine = textLine + str(paper[0]) + ',' + paper[1] + "," + str(attribute[0]) + ',' + attribute[1] + ',' + armName + "," + coder1text + ',' + coder2text + "\n"

    return [line, textLine]

# The code below runs the checkcodeset function to check that there are no issues with the codesets. If there is more than one pair, the script
# compares the first and second JSON file for each coder.

if len(coder1JSON) > 1:
    codeFileReview1 = coder1JSON[0]
    codeFileReview2 = coder2JSON[0]
    comparisonText = checkCodesets(codeFileReview1, codeFileReview2)
    file = open('fileComparison.txt', 'w')
    file.write(comparisonText)
    file.close()
else:
    comparisonText = checkCodesets(coder1JSON[0], coder2JSON[0])
    file = open('fileComparison.txt', 'w')
    file.write(comparisonText)
    file.close()

topLine = "paperID,shortTitle,AttributeId,AttributeTitle,ArmTitle,Coder1Text,Coder2Text\n"

allLines = []
textAllLines = []

# The below code produces binary and text csv strings for each pair of JSON files using the produceCsv function and writes these to two txt files

for i in range(len(coder1JSON)):

    newLines = produceCsv(coder1JSON[i], coder2JSON[i])[0]
    newTextLines = produceCsv(coder1JSON[i], coder2JSON[i])[1]

    if i == 0:
        allLines = topLine + newLines
        textAllLines = topLine + newTextLines

    else:

        allLines = allLines + newLines
        textAllLines = textAllLines + newTextLines


file = open('IrrSpreadsheetBinary.csv', 'w', encoding="utf8")

file.write(allLines)

file.close()

file = open('IrrSpreadsheetText.csv', 'w', encoding="utf8")

file.write(textAllLines)

file.close()

# The below code reads the binary csv into a new format

file = open('IrrSpreadsheetBinary.csv')

allLines = file.readlines()

file.close()


allLines = allLines[1:]

csvDataList = []
listOfAttributes = []

coder1Inclusive = []
coder2Inclusive = []

#   the belows loops over the inputted csv file and creates an ordered list for each coder with binary values
#   corresponding to particular annotations for an entity

for i in allLines:
    line = i.rstrip('\n')
    line = line.split(",")
    coder1Inclusive.append(int(line[5]))
    coder2Inclusive.append(int(line[6]))
    csvDataList.append(line)

    if line[3] not in listOfAttributes:
        listOfAttributes.append(line[3])

allCodesInclusive = [coder1Inclusive, coder2Inclusive]

listOfAttributesWithAnnotations = []

# the below creates a list of only the values that have been annotated at least once

for attribute in listOfAttributes:
    for line in csvDataList:
        if line[3] == attribute and (line[5] == '1' or line[6] == '1') and (attribute not in listOfAttributesWithAnnotations):
            listOfAttributesWithAnnotations.append(attribute)

#   the below creates a dictionary where each attribute has a key with a value which is one ordered list for each coder
#   representing binary values of their annotations

tablesForAttributes = {}
coder1Values24 = []
coder2Values24 = []
for annotatedAttribute in listOfAttributesWithAnnotations:
    coder1Values = []
    coder2Values = []
    for line in csvDataList:
        if annotatedAttribute == line[3]:
            coder1Values.append(int(line[5]))
            coder2Values.append(int(line[6]))
            coder1Values24.append(int(line[5]))
            coder2Values24.append(int(line[6]))
    tablesForAttributes[annotatedAttribute] = [coder1Values, coder2Values]

values24 = [coder1Values24, coder2Values24]

# the below creates a dictionary which gives the associated alpha value for each attribute

alphaValues = {}

for annotatedAttribute in listOfAttributesWithAnnotations:
    alphaValues[annotatedAttribute] = krippendorff.alpha(reliability_data=tablesForAttributes[annotatedAttribute], level_of_measurement='nominal')

# the below calculates overall alpha values including all attributes, and including only attributes with at least one annotation

overallValueAllAttributes = krippendorff.alpha(reliability_data=allCodesInclusive, level_of_measurement='nominal')

overallValueAnnotatedAttributes = krippendorff.alpha(reliability_data=values24, level_of_measurement='nominal')

alphaValues['All Entities'] = overallValueAllAttributes
alphaValues['Entities with data'] = overallValueAnnotatedAttributes

#   the below prints the results to a csv file

with open(resultsFileName, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
    writer.writerow(['attributes', 'alpha values'])
    for key, value in alphaValues.items():
        #print(key)
        writer.writerow([key.replace(';;;;', ','), value])