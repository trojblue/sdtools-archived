"""
小的helper
可以提取出来重复使用的methods
task-specific的东西放在原先的py里
"""
import glob
import os
import random
import inspect
import shutil
from datetime import datetime
from typing import List, Dict
import pyperclip

from sdtools.fileops import *
from sdtools.globals import *
import sdtools.fileops

def get_random_seed():
    return random.randint(0, 4294967295)

# 当前method名
curr_method_str = lambda: inspect.stack()[1][3]


def random_select(weighted_dict):  # 02a
    """d = {'1girl': 5859, 'eyes': 61, 'fur': 53}
    按权重随机选择一个词条输出
    """
    total_weight = sum(weighted_dict.values())
    r = random.randint(1, total_weight)
    for char, weight in weighted_dict.items():
        r = r - weight
        if r <= 0:
            return char


def mkdir_if_not_exist(dir: str):
    """mkdir if not exist"""
    if not os.path.exists(dir):
        os.makedirs(dir)


def remove_dupe(the_list: List) -> List:
    """输入list, 返回去重版"""
    return list(dict.fromkeys(the_list))

def paste_list_to_clipboard(prompt_list):
    clipboard = ""
    for p in prompt_list:
        clipboard += p + "\n"

    pyperclip.copy(clipboard[:-1])  # 复制到剪贴板, 去掉最后一个\n
    spam = pyperclip.paste()
    print("已复制%d行到剪贴板" % len(prompt_list))



def move_images(src_dir, dir_out):
    """把src_dir内的图片全部移动到dir_out
    """
    # create output directory if it does not exist
    if not os.path.exists(dir_out):
        os.makedirs(dir_out)

    # get mecha_tags list of all image paths in the input directory
    image_paths = [os.path.join(src_dir, i) for i in sdtools.fileops.get_files_with_suffix(src_dir, ALL_IMGS)]

    # loop through the list of image paths
    for image_path in image_paths:
        # get the file name of the image
        filename = os.path.basename(image_path)
        # move the image to the output directory
        shutil.move(image_path, os.path.join(dir_out, filename))


def get_time_str():
    return datetime.now().strftime("%y.%m.%d_%H%M")