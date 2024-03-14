import os, glob
import untangle

directory = "C:\\temp\\dnd-rulebooks\\images\\cleaned_images\\xml-nocontours"

xml_files = glob.glob(os.path.join(directory, '*e9_*.xml'))
# xml_files = glob.glob(os.path.join(directory, '*.xml'))

for xml_file in sorted(xml_files, key=lambda name: int(os.path.basename(name)[5:-6])):
    # print(xml_file)
    xml = untangle.parse(xml_file)
    print(f"Number under alto: {len(xml.alto)}") 
    print(f"Number under Layout: {len(xml.alto.Layout)}") 
    print(f"Number under Page: {len(xml.alto.Layout.Page)}") 
    print(f"Number under PrintSpace: {len(xml.alto.Layout.Page.PrintSpace)}") 
    if len(xml.alto.Layout.Page.PrintSpace) != 1:
        print(f"File: {xml_file} - Number of print spaces: {len(xml.alto.Layout.Page.PrintSpace)}") 
        # print(xml.alto.Layout.Page.PrintSpace)

        
    # print(f"Number of pages: {len(xml.alto.Layout.Page)}")


