import xml.etree.ElementTree as ET

def parse_xml(xml_file):
    # Parse XML with ElementTree
    tree = ET.parse(xml_file)
    root = tree.getroot()

    print("About to enter loop")
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
            # print(f'Tag: {tag}, Content: {content}, Height: {height}')
        elif tag.lower() == "string":
            content = elem.get('CONTENT')
            height = elem.get('HEIGHT')
            if line[-2:] == "-\n" and content[0].isalpha():
                print("Found a hyphen at the end of the line")
                line = line[0:-2] + content
            elif line[-2:] == ".\n":
                line = line[0:-1] + " " + content
            elif line[-2:-1] != "." and line[-1] == "\n":
                line = line[0:-1] + " " + content
            else:
                line += content

    print(line)

# Call the function with your XML file path
parse_xml('C:/temp/dnd-rulebooks/images/cleaned_images/xml-nocontours/image6_1.xml')
