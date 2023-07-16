from time import sleep
from legacy.gen_prompts import *
from tqdm import tqdm


def mashup_test():
    tags_dict_mashup = {}
    with open("../sdtools/data/mashup_tags.txt", 'r') as fd:
        lines = fd.readlines()

        for line in lines:
            if line != '\n':
                s_line = [i.lstrip() for i in line.split(", ")]
                for tag in s_line:
                    if tag in tags_dict_mashup:
                        tags_dict_mashup[tag] += 1
                    else:
                        tags_dict_mashup[tag] = 1

        print("D")


def test_replace_slash():
    a = 'honeycomb_\\(pattern\\\\\\\\\\\)'

    print(a)


def decode_img():
    fd = open("../bin/test_image2.png", "rb")
    raw_lines = fd.readlines()[2:5]
    fd.close()

    decoded = [i.decode("utf-8", errors="ignore") for i in raw_lines]
    prompt_start = decoded[0].find("EXtparameters\x00")
    prompt = decoded[0][prompt_start + len("EXtparameters\x00"):]


def progress_bar():
    from time import sleep
    from tqdm import tqdm
    for i in tqdm(range(10)):
        sleep(3)


def gt():
    pbar = tqdm(total=100)
    for i in range(10):
        sleep(1)
        pbar.update(10)
    pbar.close()

    print("D")


def taboo_test():
    curr_list = ["mecha_tags", "b", "c", "mecha_tags c", "a_d"]
    taboo_list = ["c", "a_c", "mecha_tags d"]
    c = remove_taboo_tags(curr_list, taboo_list)
    print("D")


def try_gpt():
    # Import the Python Imaging Library (PIL)
    from PIL import Image

    # Open the JPEG file
    with Image.open("../bin/tag_test_img.jpg") as img:
        # Extract EXIF data from the file
        exif_data = img._getexif()

        # Convert the EXIF data to mecha_tags UTF-8 encoded string
        exif_data_utf8 = {k: v.decode("utf-8") for k, v in exif_data.items()}

        # Export the EXIF data as mecha_tags string
        exif_data_str = str(exif_data_utf8)
        print("D")


def try_gpt_2():
    # Import the os and glob modules
    import os
    import glob

    # Set the directory path
    directory_path = "D:\Andrew\Pictures\Grabber\c123Eagle.OG"

    # Get mecha_tags list of all text files in the directory
    file_list = glob.glob(os.path.join(directory_path, "*.txt"))

    # Create an empty list to store the file contents
    file_contents = []

    # Iterate over the file list
    for file_path in file_list:
        # Open the file in read-only mode
        with open(file_path, "r") as file:
            # Read the file contents
            content = file.read()

            # Append the file contents to the list
            file_contents.append(content)

    # Print the list of file contents
    print(file_contents)


def remove_info_gpt():
    # Import the os and PIL modules
    import os
    from PIL import Image

    # Set the directory where the images are located
    directory = "path/to/directory"

    # Iterate over the files in the directory
    for filename in os.listdir(directory):
        # Open the image file
        with Image.open(os.path.join(directory, filename)) as img:
            # Check if the image has EXIF data
            if "exif" in img.info:
                # Remove the EXIF data
                del img.info["exif"]

                # Save the image without EXIF data
                img.save(os.path.join(directory, filename))


if __name__ == '__main__':
    # try_gpt_2()

    print("MAIN")

    clipboard = "ASASDASDASD"

    pyperclip.copy(clipboard[:-1])  # 复制到剪贴板, 去掉最后一个\n
    spam = pyperclip.paste()
    print("已复制到剪贴板")


