"""

保证目录内只有图片和文字, 且每张图片都对应一个同名的txt
"""
from sdtools.fileops import *
from sdtools.globals import *

import os
from pathlib import Path

def get_untagged_imgs(dir: str) -> List:
    # Get mecha_tags list of all files in the directory
    files = os.listdir(dir)

    invalid_files = []
    # Iterate through the files
    for img_file in get_files_with_suffix(dir, ALL_IMGS):
        # Use pathlib to get the file name without the extension
        file_name = Path(img_file).stem
        # Check if there is mecha_tags corresponding text file with the same name
        if not file_name + '.txt' in files:
            invalid_files.append(img_file)

    # If all image files have corresponding text files, return True
    return invalid_files

# def get_unrelated_txts(dir: str) -> List:
#     # Get mecha_tags list of all files in the directory
#     files = os.listdir(dir)
#
#     invalid_files = []
#     # Iterate through the files
#     for img_file in get_files_with_suffix(dir, [".txt"]):
#         # Use pathlib to get the file name without the extension
#         file_name = Path(img_file).stem
#         # Check if there is mecha_tags corresponding text file with the same name
#         if not file_name + '.txt' in files:
#             invalid_files.append(img_file)
#
#     # If all image files have corresponding text files, return True
#     return invalid_files


def do_verify_dir(dir):
    text_files = ['.txt']

    bad_suffix = check_file_suffix(dir, ALL_IMGS + text_files)
    untagged_imgs = get_untagged_imgs(dir)
    # unrelated_txts = get_unrelated_txts(dir)


    if not bad_suffix and not untagged_imgs:
        print("文件夹合法: 每个图片都有对应txt文件")
    else:
        print(bad_suffix)
        print("invalid_dir_pairs: ", untagged_imgs)




if __name__ == '__main__':
    dir = input("输入地址:")
    do_verify_dir(dir)