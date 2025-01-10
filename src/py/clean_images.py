import os, glob

from PIL import Image, ImageFilter, ImageEnhance

def process_image(input_image_path, output_image_path):
    # Open the image
    img = Image.open(input_image_path)

    # Increase contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)  # Increase contrast. The factor 1.5 is just an example.

    # Reduce noise by defining the threshold
    img = img.point(lambda p: p > 50 and 255)  # Set the threshold to 50 as an example

    # Improve sharpness
    img = img.filter(ImageFilter.SHARPEN)

    # Save the image
    img.save(output_image_path)

img_directory = "c:/temp/dnd-rulebooks/images"

# jpg_files = glob.glob(os.path.join(img_directory, '*.jpg'))
jpg_files = [os.path.join(img_directory, "image039_1.jpg")]

for file in jpg_files:
    # Use the function
    outfile = os.makedirs(os.path.join(img_directory, "clean-test", os.path.basename(file)))
    print(f"{file} -> {outfile}")
    # process_image(file, os.path.join(img_directory, ""))
