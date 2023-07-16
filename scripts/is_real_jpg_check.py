from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile

import imghdr

def is_jpeg(filepath):
    # Check the file type of the given file
    file_type = imghdr.what(filepath)

    a = Image.open(filepath)

    # Return True if the file type is JPEG, False otherwise
    return file_type == 'jpeg'



def check_image():
    path = "D:\Andrew\Pictures\=训练扩充COMBINED\\-1c72e800506fa23.jpg"
    path = "D:\Andrew\Pictures\=训练扩充COMBINED\\nogjpg\\NOT_JPEG.jpg"
    path = "D:\Andrew\Pictures\=训练扩充COMBINED\BADFORMAT\\c0911b1b8da313d.gif"

    is_jpeg(path)
    targetImage = JpegImageFile(path)


    print("D")


if __name__ == '__main__':
    check_image()