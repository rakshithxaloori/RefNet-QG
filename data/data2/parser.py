# Python 3 file

import json
import os
import sys
import ast
from copy import deepcopy

from remove import remove_extra_white_spaces

if len(sys.argv) != 6:
    sys.exit(
        "Usage: python parser.py data_json_file question_answer_file data\'s_type language_two_letter_code index")

jsonFilePath = sys.argv[1]
answerQuestionPath = sys.argv[2]
dataType = sys.argv[3]
language_code = sys.argv[4]
index = sys.argv[5]

# Create a parsed data directory
parsedDirectoryPath = os.getcwd() + os.sep + "parsedData"
try:
    os.mkdir(parsedDirectoryPath)
except OSError as error:
    print(error)

# Create a directory for the language
languageParsedDirectoryPath = parsedDirectoryPath + os.sep + language_code
try:
    os.mkdir(languageParsedDirectoryPath)
except OSError as error:
    print(error)

# Create a directory for data type
filesCommonPath = languageParsedDirectoryPath + os.sep + dataType
try:
    os.mkdir(filesCommonPath)
except OSError as error:
    print(error)

# Defining the files path
filesCommonPath = os.path.join(languageParsedDirectoryPath, dataType)

questionFilePath = filesCommonPath + os.sep + dataType + "_question.txt"
answerFilePath = filesCommonPath + os.sep + dataType + "_answer.txt"
documentFilePath = filesCommonPath + os.sep + dataType + "_document.txt"

# Deleting the files if previously exist
if os.path.exists(questionFilePath):
    os.remove(questionFilePath)

if os.path.exists(answerFilePath):
    os.remove(answerFilePath)

if os.path.exists(documentFilePath):
    os.remove(documentFilePath)

count = 0

# Read each line from that json file
with open(jsonFilePath, 'r') as jsonFile, open(documentFilePath, 'a+') as documentFile:
    # Each line is a list of dicts
    eachLine = jsonFile.readline()
    while eachLine != '':
        count += 1
        print("Document - reading the line ", count)
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

count = 0
# Read answers and questions
with open(answerQuestionPath, 'r') as answerQuestionFile, open(answerFilePath, 'a+') as answerFile, open(questionFilePath, 'a+') as questionFile:
    eachLine = answerQuestionFile.readline()
    while eachLine != '':
        count += 1
        print("Answer, question - reading the line ", count)
        questionAnswerDict = ast.literal_eval(eachLine)
        # Add the question to the file
        questionFile.write(questionAnswerDict["question"])
        questionFile.write("\n")

        # Write all the answers
        answerFile.write("[")
        for answer in questionAnswerDict["answers"]:
            answerFile.write(answer)
            answerFile.write(", ")
        answerFile.write("]")
        answerFile.write("\n")

        eachLine = answerQuestionFile.readline()