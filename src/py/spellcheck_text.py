import os
import glob
import re
from extract import spell_check
from path_utils import makedir

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

def spellcheck_files(directory):
    # Use glob to get all the text files in the directory
    text_files = glob.glob(os.path.join(directory, '*.txt'))

    full_text = ""

    for text_file in sorted(text_files, key=lambda name: int(os.path.basename(name)[5:-6])):
        print(text_file)
        # file_name_prefix = text_file.split('.')[0:-1]
        # print(output_file)

        # Read the original text
        with open(text_file, 'r') as f:
            text = f.read()
        full_text += text

    # Replace newlines with spaces
    # text = re.sub('(?<!\n)\n(?!\n)', ' ', text)
    full_text = cleanup(full_text)
    _, misspelled_words = spell_check(full_text)

    from spellchecker import SpellChecker
    spell = SpellChecker()

    makedir(os.path.join(directory, "cleaned"))
    misspelled_file = os.path.join(directory, "cleaned", "misspelled.txt")
    with open(misspelled_file, 'w') as file:
        for word in misspelled_words:
            correction = spell.correction(word)
            print(f"{word} -> {correction}")
            file.write(f"{word},{correction}\n")

    # Write the new text back to the file
    # output_file = os.path.join(directory, "cleaned", "all_text_cleaned.txt")
    # with open(output_file, 'w') as f:
    #     f.write(full_text)


# Test the function
spellcheck_files("C:\\temp\\dnd-rulebooks\\images\\cleaned_images\\trimmed-text-nocontours")
