import os, re
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps

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

        # Create labels for images
        self.original_image_view = tk.Label(self.image_frame)
        self.original_image_view.pack(expand=True)

        self.processed_image_view = tk.Label(self.processed_frame)
        self.processed_image_view.pack(expand=True)

        # Create navigation buttons

        self.next_button = tk.Button(self.image_frame, text="Next", command=self.show_next_image)
        self.next_button.pack(side=tk.BOTTOM, pady=5)

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
        self.current_image_index = 0
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
            image = Image.open(image_path)
            # Example processing: Convert image to grayscale
            processed_image = ImageOps.grayscale(image)
            width, height = processed_image.size
            processed_image = processed_image.resize((750, int(750 * height / width)))  # Maintain aspect ratio
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
