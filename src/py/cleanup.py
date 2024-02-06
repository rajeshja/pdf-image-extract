import os
import glob
import re

def join_hyphenated_words(text):
    return re.sub('-\n', '', text)

def join_broken_lines(text):
    return re.sub('(?<=[^.:\n])\n', ' ', text)

cleanup_functions = [
    join_hyphenated_words,
    join_broken_lines
]

def cleanup(text):
    for function in cleanup_functions:
        text = function(text)
    return text

def cleanup_files(directory):
    # Use glob to get all the text files in the directory
    text_files = glob.glob(os.path.join(directory, '*.txt'))

    output_file = os.path.join("all_text_cleaned.txt")
    full_text = ""

    for text_file in text_files:
        # file_name_prefix = text_file.split('.')[0:-1]
        # print(output_file)

        # Read the original text
        with open(text_file, 'r') as f:
            text = f.read()
        full_text += text

    # Replace newlines with spaces
    # text = re.sub('(?<!\n)\n(?!\n)', ' ', text)
    full_text = cleanup(full_text)

    # Write the new text back to the file
    with open(output_file, 'w') as f:
        f.write(full_text)


# Test the function
cleanup_files("c:/temp/dnd-rulebooks/images/text")
