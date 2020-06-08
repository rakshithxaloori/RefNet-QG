# Takes the parsed data
# Create json file with each data, "src" as key has context, "[SEP]", answer and "tgt" as key has question.
import sys
import os
import json
# from cltk.tokenize.word import WordTokenizer
from nltk.tokenize import wordpunct_tokenize

if len(sys.argv) != 6:
    sys.exit(
        "Usage: python3 token_parser.py context_path question_path answer_path language data_type")

context_path = sys.argv[1]
question_path = sys.argv[2]
answer_path = sys.argv[3]
language = sys.argv[4]
data_type = sys.argv[5]

# tokenizer = WordTokenizer(language)

sep_string = "[SEP]"

data_list = list()

with open(context_path, 'r') as context_file, open(question_path, 'r') as question_file, open(answer_path, 'r') as answer_file:
    # Create a json file
    # Create directory to store parsed data based on the language, dev or train in the sys.argv
    context_line = context_file.readline()
    question_line = question_file.readline()
    answer_line = answer_file.readline()
    count = 0

    while context_line != "" and question_line != "" and answer_line != "":
        print("Reading line: ", count)
        new_data = dict()

        # Tokenize these lines and add them to dict
        src_list = list()
        for word in context_line.split():
            src_list.append(word)
        
        src_list.append(sep_string)

        for word in answer_line.split():
            src_list.append(word)

        tgt_list = list()
        for word in question_line.split():
            tgt_list.append(word)

        new_data["src"] = src_list
        new_data["tgt"] = tgt_list

        # Add the dict to data
        data_list.append(new_data)
        context_line = context_file.readline()
        question_line = question_file.readline()
        answer_line = answer_file.readline()
        count += 1
    

parsed_directory_path = os.getcwd() + os.sep + "token_parsed_data"
try:
    os.mkdir(parsed_directory_path)
except OSError as error:
    print(error)

language_parsed_directory_path = parsed_directory_path + \
    os.sep + language + "_" + data_type
try:
    os.mkdir(language_parsed_directory_path)
except OSError as error:
    print(error)

# File paths
parsed_json_path = os.path.join(
    language_parsed_directory_path, data_type + "_" + language + "_token_data.json")

# Delete the file if exists
if os.path.exists(parsed_json_path):
    os.remove(parsed_json_path)

with open(parsed_json_path, 'a+') as json_file:
    for each_data in data_list:
        json.dump(each_data, json_file, ensure_ascii=False)
        json_file.write("\n")
