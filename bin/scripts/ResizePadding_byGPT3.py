# Import the PIL library
from PIL import Image

# Import the os module
import os

# Ask the user for the directory containing the images
IMAGE_DIRECTORY = "E:/grabber/test"

# Define the maximum size for the images
MAX_SIZE = (1024, 1024)

# Change the current working directory to the image directory
os.chdir(IMAGE_DIRECTORY)

# Iterate over all the files in the image directory
for file_name in os.listdir():
    # Check if the file is an image
    if file_name.endswith('.jpg') or file_name.endswith('.png'):
        # Open the image file
        image = Image.open(file_name)

        # Get the original size of the image
        width, height = image.size

        # Calculate the new size of the image
        if width > height:
            new_width = MAX_SIZE[0]
            new_height = int(height * (new_width / width))
        else:
            new_height = MAX_SIZE[1]
            new_width = int(width * (new_height / height))

        # Resize the image
        image = image.resize((new_width, new_height), Image.LANCZOS)

        # Create mecha_tags white background
        background = Image.new('RGB', MAX_SIZE, (255, 255, 255))

        # Calculate the offset to center the image on the background
        offset = ((MAX_SIZE[0] - new_width) // 2, (MAX_SIZE[1] - new_height) // 2)

        # Paste the image onto the background
        background.paste(image, offset)

        # Save the resized image
        background.save(file_name)
