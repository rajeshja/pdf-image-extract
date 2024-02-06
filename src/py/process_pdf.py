import os
import fitz

from extract import ocr_from_bytes, save_text, save_image
from path_utils import makedir

# Output directory for the extracted images
output_dir = "c:/temp/dnd-rulebooks/images"
text_subdir = "text"
# Desired output image format
output_format = "jpeg"
# Minimum width and height for extracted images
min_width = 100
min_height = 100

unique_misspelled_words = set()
# Create the output directory if it does not exist
makedir(output_dir)
makedir(os.path.join(output_dir, text_subdir))

book1 = 'G:/My Drive/RPG/AD&D 5e - Player\'s Handbook - Wizards of the Coast.pdf'

pdf_file = fitz.open(book1)

for page_index in range(len(pdf_file)):
    images = pdf_file[page_index].get_images(full=True)
    # if images:
    #     print(f"Found {len(images)} images on page {page_index+1}")

    for image_index, image in enumerate(images, start=0):
        extracted_image = pdf_file.extract_image(image[image_index])
        # print(f"Image is: {extracted_image['width']} x {extracted_image['height']}")
        image_bytes = extracted_image["image"]
        image_ext = extracted_image["ext"]
        # print(f"Page {page_index}, Extension is {image_ext}")
        file_name_base = f"image{str(page_index+1).zfill(3)}_{image_index+1}"

        page_text = ocr_from_bytes(image_bytes, extracted_image['width'], extracted_image['height'])
        # page_text, misspelled_words = spell_check(page_text)
        # unique_misspelled_words |= misspelled_words
        # print(unique_misspelled_words)
        # print(f"Writing text to: {os.path.join(output_dir, 'text', file_name_base)}.txt")
        save_text(os.path.join(output_dir, text_subdir, file_name_base), page_text)

        save_image(os.path.join(output_dir, file_name_base), image_ext, min_width, min_height, image_bytes)
