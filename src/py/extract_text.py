import cv2
import numpy as np
import pytesseract
from pytesseract import Output
from PIL import Image

def ocr_from_image(image_path):
    # Load the image from file
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use adaptive thresholding to convert the image to binary
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort the contours top-to-bottom (since that's the order text would be in)
    contours.sort(key=lambda contour: cv2.boundingRect(contour)[1])

    # Perform OCR on each contour
    text = ""
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        roi = gray[y:y+h, x:x+w]
        text += pytesseract.image_to_string(roi)

    return text
