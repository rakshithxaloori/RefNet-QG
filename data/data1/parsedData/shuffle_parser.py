# Create shuffled data from the context, answer and question files
import sys
import os
from random import shuffle

if len(sys.argv) != 7:
    sys.exit(
        "Usage: python3 shuffle_parser.py context_path question_path answer_path language data_type duplicate_count")

context_path = sys.argv[1]
question_path = sys.argv[2]
answer_path = sys.argv[3]
language = sys.argv[4]
data_type = sys.argv[5]
duplicate_count = int(sys.argv[6])


sep_string = "[SEP]"
qs_string = "[QS]"

data_list = list()

with open(context_path, 'r') as context_file, open(question_path, 'r') as question_file, open(answer_path, 'r') as answer_file:
    context_line = context_file.readline()
    question_line = question_file.readline()
    answer_line = answer_file.readline()
    count = 0

    while context_line != "" and question_line != "" and answer_line != "":
        print("Reading line: ", count)
        new_data = context_line + sep_string + answer_line + qs_string + question_line

        # Add the concat string to data
        data_list.append(new_data)
        context_line = context_file.readline()
        question_line = question_file.readline()
        answer_line = answer_file.readline()
        count += 1

duplicated_data_list = list()
# Duplicate the strings
for i in range(1, duplicate_count+1):
    print("Duplicating ", i)
    duplicated_data_list += data_list

# Shuffle the strings
shuffle(duplicated_data_list)

shuffle_directory_path = os.getcwd() + os.sep + "shuffle_data"
try:
    os.mkdir(shuffle_directory_path)
except OSError as error:
    print(error)

language_shuffle_directory_path = shuffle_directory_path + \
    os.sep + language + "_" + data_type
try:
    os.mkdir(language_shuffle_directory_path)
except OSError as error:
    print(error)

# File paths
context_shuffle_file_path = os.path.join(
    language_shuffle_directory_path, data_type + "_" + language + "_context.txt")
answer_shuffle_file_path = os.path.join(
    language_shuffle_directory_path, data_type + "_" + language + "_answer.txt")
question_shuffle_file_path = os.path.join(
    language_shuffle_directory_path, data_type + "_" + language + "_question.txt")

# Delete the file if exists
if os.path.exists(context_shuffle_file_path):
    os.remove(context_shuffle_file_path)

if os.path.exists(answer_shuffle_file_path):
    os.remove(answer_shuffle_file_path)

if os.path.exists(question_shuffle_file_path):
    os.remove(question_shuffle_file_path)

with open(context_shuffle_file_path, 'w') as context_shuffle_file, open(answer_shuffle_file_path, 'w') as answer_shuffle_file, open(question_shuffle_file_path, 'w') as question_shuffle_file:
    # Write the shuffled data to these files
    for each_data in duplicated_data_list:
        # Split into context, answer, question
        split_string = each_data.split(sep_string)
        context_string = split_string[0]

        split_string = split_string[1].split(qs_string)
        answer_string = split_string[0]
        question_string = split_string[1]

        # Add the strings to respective files
        context_shuffle_file.write(context_string)

        answer_shuffle_file.write(answer_string)

        question_shuffle_file.write(question_string)
