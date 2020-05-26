# Python 3 file

import json
import os
import sys
from copy import deepcopy

from remove import remove_non_language, remove_numbers

# Generalize for dev, train from sys.argv
if len(sys.argv) != 5:
    sys.exit(
        "Usage: python parser.py data_json_file data\'s_type language language_two_letter_code")

jsonFileName = sys.argv[1]
dataType = sys.argv[2]
language = sys.argv[3]
language_code = sys.argv[4]

with open(os.path.join(os.getcwd(), jsonFileName)) as f:
    data = json.load(f)

# List of dicts with keys title, paragraphs
# data["data"]

# The list of data of the language
data_list = list()

# Create directory to store parsed data based on the language, dev or train in the sys.argv
parsedDirectoryPath = os.getcwd() + os.sep + "parsedData"
try:
    os.mkdir(parsedDirectoryPath)
except OSError as error:
    print(error)

languageParsedDirectoryPath = os.getcwd() + os.sep + "parsedData" + \
    os.sep + language + "_" + dataType
try:
    os.mkdir(languageParsedDirectoryPath)
except OSError as error:
    print(error)

# Deleting the files if they already exist
if os.path.exists(os.path.join(languageParsedDirectoryPath, dataType + "_" + language + "_data.json")):
    os.remove(os.path.join(languageParsedDirectoryPath,
                           dataType + "_" + language + "_data.json"))

if os.path.exists(os.path.join(languageParsedDirectoryPath, dataType + "_context")):
    os.remove(os.path.join(languageParsedDirectoryPath, dataType + "_context"))

if os.path.exists(os.path.join(languageParsedDirectoryPath, dataType + "_question")):
    os.remove(os.path.join(languageParsedDirectoryPath, dataType + "_question"))

if os.path.exists(os.path.join(languageParsedDirectoryPath, dataType + "_answer")):
    os.remove(os.path.join(languageParsedDirectoryPath, dataType + "_answer"))

for eachData in data["data"]:
    # Add the language constraint
    if eachData["paragraphs"][0]["qas"][0]["id"].find(language) == -1:
        continue
    # title
    # paragraphs --> list of dicts
        # qas  --> list of dicts
            # question
            # answers --> list of dicts
            # id
        # context

    # Creating a list of data with the specified language
    copiedEachData = deepcopy(eachData)
    # Removing non-language words
    data_list.append(remove_non_language(
        copiedEachData["paragraphs"][0]["context"], language_code))

    contextFile = open(os.path.join(
        languageParsedDirectoryPath, dataType + "_context"), 'a+')
    questionFile = open(os.path.join(
        languageParsedDirectoryPath, dataType + "_question"), 'a+')
    answerFile = open(os.path.join(
        languageParsedDirectoryPath, dataType + "_answer"), 'a+')

    for paragraph in eachData["paragraphs"]:
        for qa in paragraph["qas"]:
            # Append to the three files
            # Context file -- paragraph[context]
            sentence = paragraph["context"]
            sentence = remove_numbers(sentence)
            contextFile.write(remove_non_language(sentence, language_code))
            contextFile.write('\n')

            # Questions file -- qa["question"]
            questionFile.write(qa["question"])
            questionFile.write('\n')

            # Answers file -- qa["answers"][0]["text"] -- choosing the first answer
            answerFile.write(qa["answers"][0]["text"])
            answerFile.write('\n')

    # Closing the files
    contextFile.close()
    questionFile.close()
    answerFile.close()

with open(os.path.join(languageParsedDirectoryPath, dataType + "_" + language + "_data.json"), 'w') as json_file:
    data = dict()
    data["data"] = data_list
    json.dump(data, json_file, ensure_ascii=False)
