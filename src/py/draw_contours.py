import os
import glob

import cv2
import numpy as np

from extract import ocr_from_cv_image, save_text
from path_utils import makedir

img_directory = "c:/temp/dnd-rulebooks/images/cleaned_images"
contours_directory = os.path.join(img_directory, "contours")

makedir(contours_directory)

jpg_files = glob.glob(os.path.join(img_directory, '*.jpg'))
# jpg_files = [os.path.join(img_directory, "image39_1.jpg")]

for file in sorted(jpg_files, key=lambda name: int(name.split(os.path.sep)[-1][5:-6])):
    outfile_base = '.'.join(os.path.basename(file).split('.')[0:-1])
    print(f"Processing {file} -> {outfile_base}")
    image = cv2.imread(file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = gray[0:1540, 0:gray.shape[0]]
    blur = cv2.GaussianBlur(gray, (7,7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    # binary = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    contours = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    # Create a copy of the image to draw on
    image_with_rectangles = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Draw semi-transparent rectangles on the image
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image_with_rectangles, (x, y), (x + w, y + h), (0, 0, 255, 128), 3)
    
    # Save the image with rectangles to a new directory
    cv2.imwrite(os.path.join(contours_directory, os.path.basename(file)), image_with_rectangles)