import os, re
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import cv2

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

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")
        self.root.geometry("1800x1200")  # Set a larger window size

        # Initialize variables
        self.image_list = []
        self.current_image_index = 0
        self.processed_image = None

        # Create frames for layout
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        self.image_frame = tk.Frame(self.main_frame)
        self.image_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.processed_frame = tk.Frame(self.main_frame)
        self.processed_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.prev_button = tk.Button(self.image_frame, text="Previous", command=self.show_previous_image)
        self.prev_button.pack(side=tk.TOP, pady=5)
        self.root.bind('<Left>', lambda event: self.show_previous_image())

        # Create labels for images
        self.original_image_view = tk.Label(self.image_frame)
        self.original_image_view.pack(expand=True)

        self.processed_image_view = tk.Label(self.processed_frame)
        self.processed_image_view.pack(expand=True)

        # Create navigation buttons

        self.next_button = tk.Button(self.image_frame, text="Next", command=self.show_next_image)
        self.next_button.pack(side=tk.BOTTOM, pady=5)

        self.root.bind('<Right>', lambda event: self.show_next_image())

        # Create process button
        self.process_button = tk.Button(self.main_frame, text="Process", command=self.process_image)
        self.process_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Create directory selection button
        self.select_dir_button = tk.Button(root, text="Select Directory", command=self.select_directory)
        self.select_dir_button.pack(side=tk.BOTTOM, pady=5)

        # Create a status bar
        self.status = tk.Label(root, text="No images loaded", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        # Load default directory
        self.load_default_directory()

    def load_default_directory(self):
        default_directory = 'C:/temp/dnd-rulebooks/pngs'
        if os.path.exists(default_directory):
            self.load_images(default_directory)
            self.show_image(0)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.load_images(directory)
            self.show_image(0)

    def load_images(self, directory):
        # Define a helper function to extract numbers from filenames
        def extract_number(filename):
            # Use regex to find all numbers in the filename
            numbers = re.findall(r'\d+', filename)
            # Convert found numbers to integers and return the first one (or 0 if none found)
            return int(numbers[0]) if numbers else 0

        # Load image files from the directory and sort them numerically
        self.image_list = sorted(
            [os.path.join(directory, file) for file in os.listdir(directory)
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))],
            key=lambda x: extract_number(os.path.basename(x))
        )
        self.current_image_index = 13
        self.update_status()

    def show_image(self, index):
        if self.image_list:
            image_path = self.image_list[index]
            image = Image.open(image_path)
            width, height = image.size
            image = image.resize((750, int(750 * height / width)))  # Maintain aspect ratio
            photo = ImageTk.PhotoImage(image)
            self.original_image_view.config(image=photo)
            self.original_image_view.image = photo
            self.process_image()  # Automatically process the image
            self.update_status()

    def show_next_image(self):
        if self.image_list:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_list)
            self.show_image(self.current_image_index)

    def show_previous_image(self):
        if self.image_list:
            self.current_image_index = (self.current_image_index - 1) % len(self.image_list)
            self.show_image(self.current_image_index)

    def process_image(self):
        if self.image_list:
            image_path = self.image_list[self.current_image_index]
            # Read the image using OpenCV
            image = cv2.imread(image_path)
            # Convert the image to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (7,7), 0)
            thresh = cv2.threshold(blur, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
            dilate = cv2.dilate(thresh, kernel, iterations=4)
            contours = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = contours[0] if len(contours) == 2 else contours[1]

            def are_rects_close(rect1, rect2, threshold):
                x1, y1, w1, h1 = rect1
                x2, y2, w2, h2 = rect2
                return not (x1 > x2 + w2 + threshold or x2 > x1 + w1 + threshold or
                            y1 > y2 + h2 + threshold or y2 > y1 + h1 + threshold)

            import numpy as np
            # Merge contours based on proximity
            merged_contours = []
            gap_threshold=15

            parent = list(range(len(contours)))

            def find(x):
                if parent[x] != x:
                    parent[x] = find(parent[x])
                return parent[x]

            def union(x, y):
                rootX = find(x)
                rootY = find(y)
                if rootX != rootY:
                    parent[rootY] = rootX

            # Check all pairs of contours for proximity
            for i, contour in enumerate(contours):
                if get_size(contour) == Contour_Size.SMALL:
                    continue
                x, y, w, h = cv2.boundingRect(contour)
                for j, other_contour in enumerate(contours):
                    if get_size(contour) == Contour_Size.SMALL:
                        continue
                    if i != j:
                        ox, oy, ow, oh = cv2.boundingRect(other_contour)
                        if are_rects_close((x, y, w, h), (ox, oy, ow, oh), gap_threshold):
                            union(i, j)

            # Group contours by their root parent
            from collections import defaultdict
            groups = defaultdict(list)
            for i, contour in enumerate(contours):
                root = find(i)
                groups[root].append(contour)

            # Merge contours in each group
            for group in groups.values():
                all_points = np.vstack(group)
                hull = cv2.convexHull(all_points)
                merged_contours.append(hull)

            image_with_rectangles = cv2.cvtColor(dilate, cv2.COLOR_BGR2RGB)
            # cv2.drawContours(image_with_rectangles, contours, -1, (0, 0, 255, 255), 3)

            # Draw semi-transparent rectangles on the image
            for i, contour in enumerate(merged_contours):
                x, y, w, h = cv2.boundingRect(contour)
                # is_nested = is_nested(contour, i, contours)
                cv2.rectangle(image_with_rectangles, (x+1, y+1), (x + w - 1, y + h - 1), (196, 196, 196, 64), -1)
                # cv2.rectangle(image_with_rectangles, (x, y), (x + w, y + h), (0, 255, 255, 128), 4)

            for i, contour in enumerate(contours):
                x, y, w, h = cv2.boundingRect(contour)
                # is_nested = is_nested(contour, i, contours)
                # cv2.rectangle(image_with_rectangles, (x, y), (x + w, y + h), (196, 196, 196, 128), -1)
                contour_color = get_size(contour).value
                cv2.drawContours(image_with_rectangles, [contour], 0, contour_color, 3)
                cv2.rectangle(image_with_rectangles, (x, y), (x + w, y + h), (0, 255, 255, 128), 1)

            processed_image = image_with_rectangles
            # Resize the processed image while maintaining aspect ratio
            height, width, _ = processed_image.shape
            processed_image = cv2.resize(processed_image, (750, int(750 * height / width)))
            # Convert the processed image to a format suitable for Tkinter
            processed_image = Image.fromarray(processed_image)
            self.processed_image = ImageTk.PhotoImage(processed_image)
            self.processed_image_view.config(image=self.processed_image)

    def update_status(self):
        if self.image_list:
            status_text = f"Image {self.current_image_index + 1} of {len(self.image_list)}"
        else:
            status_text = "No images loaded"
        self.status.config(text=status_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()
