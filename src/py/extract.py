import io
from PIL import Image

import cv2
import numpy as np
import pytesseract
from pytesseract import Output
from PIL import Image
import re

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

formats = {
    "png": {
        "ext": "png",
        "format": "PNG"
    },
    "jpeg": {
        "ext": "jpg",
        "format": "JPEG"
    },
    "jpx": {
        "ext": "jpg",
        "format": "JPEG"
    }
}

def ocr_from_bytes_trim(image_bytes, width, height):
    numpy_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)
    image = image[0:1540, 0:image.shape[0]]
    return ocr_from_cv_image(image, width, height)

def ocr_from_bytes(image_bytes, width, height):
    numpy_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)
    return ocr_from_cv_image(image, width, height)

def ocr_from_cv_image(cv_image, width, height):
    # print(f"Width x Height = {cv2.boundingRect(image)[2]} x {cv2.boundingRect(image)[3]}")
    larger_image= cv2.resize(cv_image, (width, height), fx=4, fy=4, interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(larger_image, cv2.COLOR_BGR2GRAY)

    # Use adaptive thresholding to convert the image to binary
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort the contours top-to-bottom (since that's the order text would be in)
    sorted_contours = sorted(contours, key=lambda contour: (cv2.boundingRect(contour)[1], cv2.boundingRect(contour)[0]))

    # Perform OCR on each contour
    text = ""
    for contour in sorted_contours:
        x, y, w, h = cv2.boundingRect(contour)
        roi = gray[y:y+h, x:x+w]
        text += pytesseract.image_to_string(roi)

    return text

def spell_check(text, custom_words = []):
    from spellchecker import SpellChecker
    spell = SpellChecker()

    # Add custom words to dictionary
    spell.word_frequency.load_words(custom_words)

    # Find all words in the text
    # words = text.split()
    # Split into words accounting for punctuation and other separators.
    words = re.findall(r'\b\w+\b', text)

    # Find those words that may be misspelled
    misspelled = spell.unknown(words)
    # print(f"Misspelt words: {misspelled}")

    # for word in misspelled:
    #     # Get the one 'most likely' answer
    #     correct = spell.correction(word)

    #     # Replace the misspelled word with the correct one in the text
    #     text = text.replace(word, correct)

    return text, misspelled

def save_text(file_name_base, page_text):
    with open(f"{file_name_base}.txt", 'w') as f:
        f.write(page_text)

def save_image(file_name_base, format, min_width, min_height, image_bytes):
    image_file = Image.open(io.BytesIO(image_bytes))
    if image_file.width >= min_width and image_file.height >= min_height:
        # print(f"Saving {file_name_base}.{formats[format]['ext']}")
        image_file.save(
                open(f"{file_name_base}.{formats[format]['ext']}","wb"),
                format = formats[format]['format'],
                quality=100,
                subsampling=0)
    else:
        print(f"Skipping small image - {image_file.width} x {image_file.height}")


# import pytesseract

# # Extract images and perform OCR on each one
# for image in page.images:
#     print(image)
#     im = Image.open(image.stream)
#     text += pytesseract.image_to_string(im)


# Test the function
# print(ocr_from_pdf())
