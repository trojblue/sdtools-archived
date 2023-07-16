"""
读取目录里所有txt, 统计词条出现次数, 按出现次数作为权重随机生成新prompt
"""
import csv
import json
import os
import random

from helpers import *
from settings import *

all_tags_list = []
weighted_tags_dict = {}
danbooru_tags_dict = {}
mutex_tags = []
mutable_tags = []

default_train_set = "D:\Andrew\Pictures\Grabber\c123Eagle.OG"

def get_json_tags():  # 01a 读取json
    global preferred_tags
    global avoided_tags

    f = open('../tags.json')
    json_data = json.load(f)
    f.close()

    for tag_name in json_data:
        if tag_name == "_comment":
            continue
        if json_data[tag_name]["type"] == "mutex":
            mutex_tags.append(tuple(json_data[tag_name]["tags"]))
        elif json_data[tag_name]["type"] == "mutable":
            mutable_tags.append(tuple(json_data[tag_name]["tags"]))


# def process_weights():  # 01b
#     """根据gen_settings.py的设置, 调整weighted_tags_dict 里的tag权重
#     """
#     f = open('tags.json')
#     json_data = json.load(f)
#     f.close()
#
#     print("Weights Processed")
#
#
# def read_mashup_tags():
#     """从bin读取mashup_tags.txt"""
#     lines = ""
#     with open("sdtools/data/mashup_tags.txt", 'r') as fd:
#         lines = fd.readlines()

# def get_danbooru_tags():
#     """从danbooru.csv读取到全局变量
#     """
#     global danbooru_tags_dict
#     with open(danbooru_csv, mode='r') as infile:
#         reader = csv.reader(infile)
#         danbooru_tags_dict = {rows[0]: rows[1] for rows in reader}


def read_files(addr: str):  # 01: 所有文件读取操作
    global all_tags_list
    all_files = os.listdir(addr)
    txt_files = filter(lambda x: x[-4:] == '.txt', all_files)  # 文件夹下的所有txt文件

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

    get_json_tags()
    # get_danbooru_tags()
    # process_weights()


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


def remove_mutex(word_list: List[str], mutex_tags: Tuple):  # 02b
    """确认word_list中只存在一个mutex_tags里包含的tag
    保留第一个, 其余的会被移除
    ***默认输入只有空格, 没有下划线***
    """
    mutex_space_list = []
    for curr_group in mutex_tags:
        if curr_group:
            curr_sublist = [a.replace("_", " ") for a in curr_group]
            [replace_duplicates(a.lstrip(), "  ", " ") for a in curr_sublist]
            mutex_space_list.append(tuple(curr_sublist))



    mutex_space = tuple(mutex_space_list)
    # mutex_underline = [a.replace(" ", "_") for a in mutex_space]  # 空格变下划线

    ListA = word_list

    in_set_count = 0
    for curr_tag in mutex_space:
        if curr_tag in word_list and in_set_count > 0:  # 已存在一个tags里面的tag
            ListA = list(filter(lambda curr: curr != curr_tag, ListA))
        else:
            in_set_count += 1

    # todo: 同时处理下划线和空格
    # in_set_count = 0
    # for curr_tag in mutex_underline:
    #     if curr_tag in word_list and in_set_count > 0:  # 已存在一个tags里面的tag
    #         ListA = list(filter(lambda curr: curr != curr_tag, ListA))
    #     else:
    #         in_set_count += 1

    return ListA


def remove_taboo_tags(curr_tags, taboo_tags) -> List:
    """去除下划线和空格方式链接的taboo tags
    """
    taboo_space = [a.replace("_", " ") for a in taboo_tags]  # 下划线变空格
    taboo_space = [replace_duplicates(a.lstrip(), "  ", " ") for a in taboo_space]  # 去除重复空格
    taboo_underline = [a.replace(" ", "_") for a in taboo_space]  # 空格变下划线

    new_tags = [i for i in curr_tags if i not in taboo_space]
    new_tags = [i for i in new_tags if i not in taboo_underline]

    return new_tags


def generate_prompt(tag_count: int) -> List[str]:  # 02 参数生成
    """读取全局tag list, 返回(单次生成)所用的完整prompts
    :param tag_count: 生成的tag数量
    """
    if not weighted_tags_dict:
        return []

    end_tags_len = len(gs.end_tags)
    new_tags = [random_select(weighted_tags_dict) for i in range(tag_count * 2)]  # 从weighted_dict随机生成2n个
    new_tags = list(dict.fromkeys(new_tags))  # 去重
    new_tags = remove_occurence_if_exists(gs.vital_tags + gs.end_tags, new_tags)  # 去除已存在的开头结尾tag

    new_tags = gs.vital_tags + new_tags  # 前部添加vital_tag
    if gs.accent_tags:                      # 添加accent
        new_tags = new_tags + random.choices(gs.accent_tags,k=gs.accent_count)

    new_tags = clean_tags(new_tags)  # 数据清理

    return new_tags[:tag_count - end_tags_len] + gs.end_tags  # 返回前n个


def clean_tags(og_tags):
    new_tags = [a.replace("_", " ") for a in og_tags]  # 下划线变空格
    new_tags = [replace_duplicates(a.lstrip(), "  ", " ") for a in new_tags]  # 去除重复空格
    # new_tags = [a.replace(" ", "_") for a in new_tags]  # 空格变下划线

    new_tags = remove_mutex(new_tags, tuple(mutex_tags))  # 去除mutex
    new_tags = [replace_duplicates(a, "\\\\", "\\") for a in new_tags]  # 去除重复斜杠
    new_tags = remove_taboo_tags(new_tags, gs.taboo_tags)  # 去除taboo
    new_tags = remove_dupe(new_tags)  # 去重
    return new_tags


def clean_tags_lite(og_tags):
        """只操作下划线, taboo只去除trash tags
        """
        new_tags = [a.replace("_", " ") for a in og_tags]  # 下划线变空格
        new_tags = [replace_duplicates(a.lstrip(), "  ", " ") for a in new_tags]  # 去除重复空格
        # new_tags = [a.replace(" ", "_") for a in new_tags]  # 空格变下划线

        new_tags = remove_mutex(new_tags, tuple(mutex_tags))  # 去除mutex
        new_tags = [replace_duplicates(a, "\\\\", "\\") for a in new_tags]  # 去除重复斜杠
        new_tags = remove_taboo_tags(new_tags, trash_tags)  # 去除taboo
        new_tags = remove_dupe(new_tags)  # 去重
        return new_tags

def generate_prompt_to_list(tag_count, line_count) -> List:
    addr = default_train_set
    tag_count = tag_count or 45
    line_count = line_count or 20

    prompt_list = []

    read_files(addr)

    for i in range(line_count):
        tags_str = ", ".join(generate_prompt(tag_count))
        prompt_list.append(tags_str)

    return prompt_list


def sese_mode():
    """45词, 随机混25个色情tag"""
    OG_list = generate_prompt(45)
    sese_tags = random.sample(SEX_TAGS, 30)
    new_list = OG_list[:10] + sese_tags + OG_list[-4:]
    new_list = clean_tags(new_list)

    return new_list


if __name__ == '__main__':
    # get_danbooru_tags()

    # addr = input("输入训练集地址:") or default_train_set
    addr = default_train_set
    tag_count = int(input("输入tag个数:") or 45)  # 下划线: 150token ≈ 40word; 空格: 45words
    line_count = int(input("输入生成行数:") or 5)

    clipboard = ""
    read_files(addr)

    for i in range(line_count):
        # tags_str = ", ".join(sese_mode())
        tags_str = ", ".join(generate_prompt(tag_count))
        clipboard += gs.start_word + tags_str + "\n"

    pyperclip.copy(clipboard[:-1])  # 复制到剪贴板, 去掉最后一个\n
    spam = pyperclip.paste()

    print("已复制%d行到剪贴板" % line_count)
