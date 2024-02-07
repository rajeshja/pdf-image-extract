import os
import glob

import cv2
import numpy as np

from extract import ocr_from_cv_image, save_text
from path_utils import makedir

from enum import Enum

class Contour_Size(Enum):
    SMALL = (0, 0, 255, 255)
    MEDIUM = (0, 255, 0, 255)
    LARGE = (255, 0, 0, 255)

def get_size(contour):
    x, y, w, h = cv2.boundingRect(contour)
    area = cv2.contourArea(contour)
    boundsArea = w*h
    areaPerc = 100*area/boundsArea
    size = Contour_Size.LARGE
    if areaPerc < 20:
        size = Contour_Size.SMALL
    elif areaPerc < 50:
        size = Contour_Size.MEDIUM
    elif boundsArea < 1000:
        size = Contour_Size.SMALL
    elif boundsArea < 5000:
        size = Contour_Size.MEDIUM

    return size

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
    # thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    # binary = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    contours = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    # Create a copy of the image to draw on
    image_with_rectangles = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # cv2.drawContours(image_with_rectangles, contours, -1, (0, 0, 255, 255), 3)

    # Draw semi-transparent rectangles on the image
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        # is_nested = is_nested(contour, i, contours)
        cv2.rectangle(image_with_rectangles, (x, y), (x + w, y + h), (0, 128, 255, 128), 3)
        contour_color = get_size(contour).value
        cv2.drawContours(image_with_rectangles, [contour], 0, contour_color, 3)
        # print(f"File: ${file.rjust(14)}: Contour# {str(i).rjust(3)}, Area: {cv2.contourArea(contour)}, Bounds Area: {w*h}, Area as % of Bounds: {cv2.contourArea(contour)*100/(w*h)}")
    # Save the image with rectangles to a new directory
    cv2.imwrite(os.path.join(contours_directory, os.path.basename(file)), image_with_rectangles)

# def is_small(contour):



def is_nested(contour, i, contours):
    # List to store rectangles within another rectangle
    # Iterate over the list of rectangles
    # Flag to check if rect1 is within another rectangle
    is_within = False

    x1, y1, w1, h1 = cv2.boundingRect(contour)    

    # Iterate over the remaining rectangles
    for j, rect2 in enumerate(contours):
        if i==j:
            continue
        x2, y2, w2, h2 = cv2.boundingRect(rect2)
        
        # Check if rect1 is completely contained within rect2
        if x2 < x1 and y2 < y1 and x2 + w2 > x1 + w1 and y2 + h2 > y1 + h1:
            is_within = True
            break
    
    # If rect1 is within another rectangle, add it to the list
    return is_within