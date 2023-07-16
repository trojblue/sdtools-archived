"""
读取目录里所有txt, 统计词条出现次数, 按出现次数作为权重随机生成新prompt
"""
import os
import random
from typing import List, Tuple

import pyperclip

from settings import *

def read_files(addr: str):  #01: 所有文件读取操作
    global all_tags_list
    all_files = os.listdir(addr)
    txt_files = filter(lambda x: x[-4:] == '.txt', all_files) # 文件夹下的所有txt文件

    for i in txt_files:
        path = addr + "\\" + i
        with open(path, 'rt') as fd:
            lines = fd.readlines()
            single_line_tags = ", ".join(lines).split(",")
            for key in single_line_tags:
                if key in weighted_tags_dict:
                    weighted_tags_dict[key] += 1
                else:
                    weighted_tags_dict[key] = 1


if __name__ == '__main__':
    addr = test_train_set

    read_files(addr)

    for i in range(line_count):
        tags_str = ", ".join(generate_prompt(tag_count))
        clipboard += tags_str + "\n"

    pyperclip.copy(clipboard[:-1])  # 复制到剪贴板, 去掉最后一个\n
    spam = pyperclip.paste()

    print("已复制%d行到剪贴板" % line_count)
