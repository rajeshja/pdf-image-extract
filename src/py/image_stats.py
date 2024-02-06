import os
import glob

import cv2
import numpy as np

directory = "c:/temp/dnd-rulebooks/images"

jpg_files = glob.glob(os.path.join(directory, '*.jpg'))

widths = set()
heights = set()

for file in jpg_files:
    image = cv2.imread(file, cv2.IMREAD_COLOR)
    widths.add(image.shape[0])
    heights.add(image.shape[1])

print("Widths:")
for width in sorted(widths):
    print(f"\t{width}")

print("Heights:")
for height in sorted(heights):
    print(f"\t{height}")