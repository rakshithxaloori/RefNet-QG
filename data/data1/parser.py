# Python 3 file

import json
import os
import sys
from copy import deepcopy

from remove import remove_non_language, remove_numbers, remove_extra_white_spaces

from nltk.tokenize import sent_tokenize
from cltk.tokenize.sentence import TokenizeSentence

# Generalize for dev, train from sys.argv
if len(sys.argv) != 5:
    sys.exit(
        "Usage: python parser.py data_json_file data\'s_type language language_two_letter_code")

jsonFileName = sys.argv[1]
dataType = sys.argv[2]
language = sys.argv[3]
language_code = sys.argv[4]

tokenizer = TokenizeSentence(language)

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

# File paths
parsedJsonFilePath = os.path.join(languageParsedDirectoryPath, dataType + "_" + language + "_data.json")
contextFilePath = os.path.join(languageParsedDirectoryPath, dataType + "_context.txt")
questionFilePath = os.path.join(languageParsedDirectoryPath, dataType + "_question.txt")
answerFilePath = os.path.join(languageParsedDirectoryPath, dataType + "_answer.txt")
answerSentenceFilePath = os.path.join(languageParsedDirectoryPath, dataType + "_answer_sentence.txt")

# Deleting the files if they already exist
if os.path.exists(parsedJsonFilePath):
    os.remove(parsedJsonFilePath)

if os.path.exists(contextFilePath):
    os.remove(contextFilePath)

if os.path.exists(questionFilePath):
    os.remove(questionFilePath)

if os.path.exists(answerFilePath):
    os.remove(answerFilePath)

if os.path.exists(answerSentenceFilePath):
    os.remove(answerSentenceFilePath)

count = 0
for eachData in data["data"]:
    # Add the language constraint
    if eachData["paragraphs"][0]["qas"][0]["id"].find(language) == -1:
        continue

    print(language.upper(), " data found!: ", count)
    count += 1

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
    context = copiedEachData["paragraphs"][0]["context"]
    # context = remove_numbers(context)
    # context = remove_non_language(context, language_code)
    context = remove_extra_white_spaces(context)
    data_list.append(context)

    contextFile = open(contextFilePath, 'a+')
    questionFile = open(questionFilePath, 'a+')
    answerFile = open(answerFilePath, 'a+')
    answerSentenceFile = open(answerSentenceFilePath, 'a+')

    for paragraph in eachData["paragraphs"]:
        for qa in paragraph["qas"]:
            # Append to the three files
            # Answers file -- qa["answers"][0]["text"] -- choosing the first answer
            answer = qa["answers"][0]["text"]
            # Find the answer in the context
            foundFlag = False
            for sentence in tokenizer.tokenize_sentences(context):
                if sentence.find(answer) != -1:
                    # Answer found
                    foundFlag = True
                    answerSentenceFile.write(sentence)
                    answerSentenceFile.write('\n')
                    break

            if not foundFlag:
                # The answer is not found
                if context.find(answer) != -1:
                    print("FOUND IN CONTEXT")
                else:
                    print("NOT FOUND")
                continue

            # Only write the answer if the answer is in the context
            answerFile.write(answer)
            answerFile.write('\n')


            # Context file -- paragraph[context]
            contextFile.write(context)
            contextFile.write('\n')

            # Questions file -- qa["question"]
            question = qa["question"]
            questionFile.write(question)
            questionFile.write('\n')



    # Closing the files
    contextFile.close()
    questionFile.close()
    answerFile.close()

with open(os.path.join(languageParsedDirectoryPath, dataType + "_" + language + "_data.json"), 'w') as json_file:
    data = dict()
    data["data"] = data_list
    json.dump(data, json_file, ensure_ascii=False)
