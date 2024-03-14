import xml.etree.ElementTree as ET

def append_content_to_line(line, content):
    if len(line) < 2:
        line += content
    elif line[-2:] == "-\n" and content[0].isalpha():
        # Fix hyphenated words
        line = line[0:-2] + content
    elif line[-2:] == ".\n" or (line[-2:-1] != "." and line[-1] == "\n"):
        # Fullstop without new paragraph (unreliable?)
        # or middle of a sentence. Remove previous newline
        # and add next word
        line = line[0:-1] + " " + content
    else:
        line += content
    return line

def parse_xml(xml_file):
    # Parse XML with ElementTree
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Iterate over each "string" element in the XML
    line = ""
    for elem in root.iter():
        # print("About to enter loop")
        tag = elem.tag.split('}')[-1]
        if tag.lower() == "textline" or tag.lower() == "textblock" or tag.lower() == "composedblock":
            line += "\n"
        elif tag.lower() == "sp":
            width = int(int(elem.get('WIDTH'))/8)
            if width == 0:
                width = 1
            for i in range(width):
                line += " "
        elif tag.lower() == "string":
            content = elem.get('CONTENT')
            height = elem.get('HEIGHT')
            line = append_content_to_line(line, content)

    return line

# Call the function with your XML file path
parse_xml('C:/temp/dnd-rulebooks/images/cleaned_images/xml-nocontours/image8_1.xml')

import os, glob

alto_directory = "c:/temp/dnd-rulebooks/images/cleaned_images/xml-nocontours"
text_directory = os.path.join(alto_directory, "alltext")

if not os.path.exists(alto_directory):
    print(f"Directory does not exist: {alto_directory}")

xmls = glob.glob(os.path.join(alto_directory, '*.xml'))

all_text = ""

for xml in sorted(xmls, key=lambda name: int(name.split(os.path.sep)[-1][5:-6])):
    all_text =  append_content_to_line(all_text, parse_xml(xml))

if not os.path.exists(text_directory):
    os.makedirs(text_directory)

with open(os.path.join(text_directory, "alltext.txt"), 'w') as file:
    file.write(all_text)

