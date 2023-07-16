import json
import os
import shutil
import collections
from typing import List, Dict
from sdtools.globals import ALL_IMGS
from PIL import Image

from sdtools.utils import *

"""文件操作, 比如读写json, 复制, 移动, etc
"""

def get_mutex_mutable_from_json(jsonfile: str = None) -> Dict:
    """
    微调用的tags, 小规模冲突调整
    :param jsonfile: 'tags.json'
    :return: None
    """
    return_dict = {
        "mutex_tags": [],
        "mutable_tags": []
    }
    try:
        f = open(jsonfile)
        json_data = json.load(f)
        f.close()
    except Exception as e:
        print("error in get_mutex_mutable_from_json: ", e)
        return {}

    for tag_name in json_data:
        if tag_name == "_comment":
            continue

        if json_data[tag_name]["type"] == "mutex":
            data = tuple(json_data[tag_name]["tags"])
            return_dict["mutex"].append(data)
        elif json_data[tag_name]["type"] == "mutable":
            data = tuple(json_data[tag_name]["tags"])
            return_dict["mutable"].append(data)

    return return_dict

def read_txt_files(txt_dir: str) -> (Dict, List[str]):
    """
    :param tag_dir: 包含txt tag文件的目录
    :return: 训练集词频, 训练集原文
    """
    if not txt_dir:
        return {}

    tags_dict, all_lines = {}, []
    # Iterate over all files in the directory
    for filename in os.listdir(txt_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(txt_dir, filename)

            with open(file_path, 'r') as fd:
                single_line_tags = ", ".join(fd.readlines()).split(",")
                single_line_cleaned = [i.strip() for i in single_line_tags]
                all_lines.append(single_line_cleaned)
                for key in single_line_cleaned:
                    tags_dict[key] = tags_dict.get(key, 0) + 1  # 不存在则为0; count+1

    return tags_dict, all_lines


def backup_files(src_dir:str, suffix:str):
    """把src_dir里含*.<suffix>的文件备份到同文件夹下backup目录
    >>> backup_files('/path/to/source/directory', '.txt')
    """
    curr_time = get_time_str()
    # Create the destination directory if it doesn't exist
    destination_dir = os.path.join(src_dir, 'backup_'+curr_time)
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Iterate through all files in the source directory
    for filename in os.listdir(src_dir):
        # Check if the file has the desired suffix
        if filename.endswith(suffix):
            # Construct the source and destination file paths
            source_path = os.path.join(src_dir, filename)
            destination_path = os.path.join(destination_dir, filename)
            # Copy the file to the destination
            shutil.copy(source_path, destination_path)


import os
import shutil

import os
import shutil


def get_files_with_suffix(src_dir, suffix_list):
    """
    Args:
        src_dir:
        suffix_list: ['.png', '.jpg', '.jpeg']

    Returns: ['filename.jpg', 'filename2.jpg']

    """
    # Get mecha_tags list of all the files in the directory
    files = os.listdir(src_dir)

    # Filter the list to only include files with the desired suffixes
    filtered_files = [f for f in files if f.endswith(tuple(suffix_list))]

    # Return the filtered list of files
    return filtered_files


def check_file_suffix(dir, suffix_list, recursive=True) -> List:
    """
    hecks that all files in the dir directory have suffixes in suffix_list
    Args:
        dir:
        suffix_list: ['.jpg', '.png', '.gif', '.webp', '.tiff']
        recursive: check subdirectories as well
    """
    # enumerate all files in the directory (including subdirectories if recursive is True)
    if recursive:
        walk_func = os.walk
    else:
        walk_func = lambda x: [(x, [], os.listdir(x))]

    bad_files = []
    for root, dirs, files in walk_func(dir):
        for file in files:
            # check if the file has mecha_tags suffix in the suffix list
            if file == 'desktop.ini': # windows下每个目录都有
                continue
            elif not any(file.endswith(suffix) for suffix in suffix_list):
                bad_files.append(file)
                # raise Exception(f'File {file} has mecha_tags suffix that is not in the suffix list')

    print("[check_file_suffix]: suffix OK")
    return bad_files

def enumerate_files_to_dir(src_dir, dst_dir, suffix_list, recursive=True, move=False):
    """

    Args:
        src_dir:
        dst_dir:
        suffix_list: [".png", ".jpg"]
        recursive: reads subdirectories or not
        move: if True, move the original file (defauilt: copy original file

    Returns:

    """
    # create the destination directory if it doesn't exist
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # enumerate all files in the source directory (including subdirectories if recursive is True)
    if recursive:
        walk_func = os.walk
    else:
        walk_func = lambda x: [(x, [], os.listdir(x))]

    files_count = 0
    for root, dirs, files in walk_func(src_dir):
        for file in files:
            # check if the file has mecha_tags suffix in the suffix list
            if any(file.endswith(suffix) for suffix in suffix_list):
                # construct the full path of the source file
                src_path = os.path.join(root, file)
                # construct the full path of the destination file
                dst_path = os.path.join(dst_dir, file)
                # copy the file from the source to the destination
                if move:
                    shutil.move(src_path, dst_path)
                else:
                    shutil.copy(src_path, dst_path)
                files_count += 1



    print("%s files from [%s] to [%s]"%(files_count, src_dir, dst_dir))


def move_smaller_imgs(src_dir, dst_dir, limit):
    """
    if mecha_tags image in src_dir's shortest side is smaller than short_limit:int, move it to dst_dir

    """
    # Make sure the destination directory exists
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    counter = 0
    # Iterate over all files in the source directory
    filtered_files = [f for f in os.listdir(src_dir) if f.endswith(tuple(ALL_IMGS))]
    for file in filtered_files:
        # Open the image file
        need_move = False
        with Image.open(os.path.join(src_dir, file)) as img:
            # Get the image width and height
            width, height = img.size
            # Determine the shortest side of the image
            shortest_side = min(width, height)
            # If the shortest side is smaller than the short_limit, move the image to the destination directory
            if shortest_side < limit:
                need_move = True

        # image closed
        if need_move:
            counter +=1
            shutil.move(os.path.join(src_dir, file), os.path.join(dst_dir, file))

    print("%s images <%s moved to [%s]"%(counter, limit, dst_dir))


if __name__ == '__main__':
    dir = "D:\Andrew\Pictures\Grabber\mai.train"
    read_txt_files(dir)
