# Python 3 file

import json
import os
import sys
import ast
from copy import deepcopy

from remove import remove_extra_white_spaces

if len(sys.argv) != 5:
    sys.exit(
        "Usage: python parser.py data_json_file data\'s_type language_two_letter_code index")

jsonFileName = sys.argv[1]
dataType = sys.argv[2]
language_code = sys.argv[3]
index = sys.argv[4]

# Create a parsed data directory
parsedDirectoryPath = os.getcwd() + os.sep + "parsedData"
try:
    os.mkdir(parsedDirectoryPath)
except OSError as error:
    print(error)

# Create a directory for the language
languageParsedDirectoryPath = os.getcwd() + os.sep + "parsedData" + \
    os.sep + language_code
try:
    os.mkdir(languageParsedDirectoryPath)
except OSError as error:
    print(error)

# Defining the files path
filesCommonPath = os.path.join(languageParsedDirectoryPath, dataType)

questionFilePath = filesCommonPath + "_question.txt"
answerFilePath = filesCommonPath + "_answer.txt"
documentFilePath = filesCommonPath + "_document.txt"

# Deleting the files if previously exist
if os.path.exists(questionFilePath):
    os.remove(questionFilePath)

if os.path.exists(answerFilePath):
    os.remove(answerFilePath)

if os.path.exists(documentFilePath):
    os.remove(documentFilePath)

count = 0

# Read each line from that json file
with open(jsonFileName, 'r') as jsonFile, open(documentFilePath, 'a+') as documentFile:
    # Each line is a list of dicts
    eachLine = jsonFile.readline()
    while eachLine != '':
        count += 1
        print("Reading the line ", count)
        jsonLine = '{' + '\"data\"' + ':' + eachLine + '}'
        jsonDict = ast.literal_eval(jsonLine)
        # Get the jsonDict["data"][itrIndex]["document"] where jsonDict["data"][itrIndex]["id"][1] == index
        itrIndex = 0
        try:
            while jsonDict["data"][itrIndex]["id"][1] == index:
                itrIndex += 1
        except IndexError:
            sys.exit("The index is too high!")

        # Add the jsonDict["data"][itrIndex]["document"] to the documentFile
        documentLine = jsonDict["data"][itrIndex]["document"]
        documentFile.write(remove_extra_white_spaces(documentLine))
        documentFile.write("\n")

        eachLine = jsonFile.readline()
