import os

# from sdtools.aug_image import convert_to_png
from sdtools.fileops import enumerate_files_to_dir
from sdtools.globals import *


def do_convert_png(src_dir, dst_dir, suffix_list):
    backup_path = os.path.join(src_dir, "UNCONVENTIONAL")
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)

    enumerate_files_to_dir(src_dir, backup_path, suffix_list, recursive=False, move=True)

    # convert images in BACKUP and copy them to dst_dir
    # NOT WORKINGwesdx4refdgvb
    # convert_to_png(str(backup_path), dst_dir, suffix_list=suffix_list)


if __name__ == '__main__':
    # 移动所有非jpg, png的文件到子文件夹UNCONVENTIONAL
    src_dir = 'D:\Andrew\Pictures\=训练扩充COMBINED'
    dst_dir = 'D:\Andrew\Pictures\=训练扩充COMBINED'
    suffix = NON_JPG_PNG_IMGS

    do_convert_png(src_dir, dst_dir, suffix)