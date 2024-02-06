import os
import glob

import cv2
import numpy as np

from extract import ocr_from_cv_image, save_text

img_directory = "c:/temp/dnd-rulebooks/images/cleaned_images"
text_directory = os.path.join(img_directory, "trimmed-text")

if not os.path.exists(text_directory):
    os.makedirs(text_directory)

jpg_files = glob.glob(os.path.join(img_directory, '*.jpg'))
# jpg_files = [os.path.join(img_directory, "image39_1.jpg")]

for i, file in enumerate(sorted(jpg_files, key=lambda name: int(name.split(os.path.sep)[-1][5:-6]))):
    outfile_base = '.'.join(os.path.basename(file).split('.')[0:-1])
    print(f"Processing {file} -> {outfile_base}")
    image = cv2.imread(file, cv2.IMREAD_COLOR)
    image = image[0:1540, 0:image.shape[0]]
    page_text = ocr_from_cv_image(image, image.shape[0], image.shape[1], i)
    save_text(os.path.join(text_directory, f"{outfile_base}"), page_text)