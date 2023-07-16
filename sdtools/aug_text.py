"""处理数据集
"""
import os
from typing import *
from legacy.settings import *
from legacy.helpers import *
from sdtools.fileops import *


def escape_brackets(tags:List[str]) -> List[str]:

    tags_str = ", ".join(tags)
    tags_str = tags_str.replace("(", "\\(")
    tags_str = tags_str.replace(")", "\\)")
    new_tags = tags_str.split(', ')
    new_tags = [replace_duplicates(a, "\\\\", "\\") for a in new_tags]

    return new_tags



def process_text(raw_line: str) -> str:
    """处理数据集文本:
    """
    # new_tags = raw_line + ", maimuro"
    new_tags = remove_dupe((raw_line).split(","))
    # clip_string = max(enumerate(new_tags), key=lambda x: len(x[1]))  # clip描述的string, 似乎不行

    new_tags = [replace_duplicates(a.lstrip(), "  ", " ") for a in new_tags]  # 去除重复空格
    new_tags = [replace_duplicates(a.lstrip(), ",,", ",") for a in new_tags]  # 去除重复逗号

    # new_tags = [mecha_tags.replace(" ", "_") for mecha_tags in new_tags]                      # 空格变下划线
    new_tags = [a.replace("_", " ") for a in new_tags]                      # 下划线变空格

    new_tags = escape_brackets(new_tags)

    new_tags = remove_occurence_if_exists(trash_tags, new_tags)  # 去垃圾tag
    # new_tags[int(clip_string[0])] = clip_string[1]                          # clip恢复无下划线
    new_tags = remove_occurence_if_exists(trash_tags, new_tags)  # 去垃圾tag
    new_tags = [replace_duplicates(a, ", , ", ", ") for a in new_tags]    # 去掉空tag
    new_tags = [replace_duplicates(a.lstrip(), ",,", ",") for a in new_tags]  # 去除重复逗号
    out_string = ", ".join(new_tags)

    return out_string


def process_text_temp(raw_line: str) -> str:
    """只添加by sks"""
    out_string = raw_line + ", by sks"
    return out_string


def clean_folder(addr: str):
    """
    清洗<addr>内的所有文本文档
    **注意会覆盖原文件, 最好先备份**
    """
    all_files = os.listdir(addr)
    txt_files = filter(lambda x: x[-4:] == '.txt', all_files)  # 文件夹下的所有txt文件
    counter = 0

    for i in txt_files:
        path = addr + "\\" + i
        with open(path, 'rt') as fd:
            one_liner = ", ".join(fd.readlines())
            out_line = process_text(one_liner)  # 关键步骤

        with open(path, 'w') as f:
            f.write(out_line)
        counter += 1

    print("已处理 %d个文本" % counter)


if __name__ == '__main__':
    addr = "D:\Andrew\Pictures\Grabber\mai.train"
    backup_files(addr, '.txt')
    clean_folder(addr)
