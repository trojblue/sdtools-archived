import random
from typing import List, Tuple
from sdtools import globals
import sdtools.utils as utils


def replace_duplicates(my_str, old: str, new: str) -> str:
    """把my_str里的<old>递归替换为<new>"""
    a_curr, a_new = my_str, my_str
    a_new = a_curr.replace(old, new)
    while a_new != a_curr:
        a_curr = a_new
        a_new = a_curr.replace(old, new)
    return a_new


def remove_occurence_if_exists(remove_list, from_list) -> List:
    """从from_list里删除remove_list里的元素
    假设tag不会重复
    """
    unique_rl = list(dict.fromkeys(remove_list))
    new_list = [i for i in from_list]
    for r in unique_rl:
        try:
            new_list.remove(r)
        except Exception:
            continue
    return new_list


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


def clean_tags(sdt, og_tags: List[str], lite_mode=False) -> List[str]:
    """
    :param sdt:
    :param og_tags:
    :param lite_mode: True时只去掉最少量的tag; 否则则根据设定去掉sdt里的taboo_tags
            taboo_tag里已经包含了trash_tag
    :return:
    """
    new_tags = [a.replace("_", " ") for a in og_tags]  # 下划线变空格
    new_tags = [replace_duplicates(a.lstrip(), "  ", " ") for a in new_tags]  # 去除重复空格
    # new_tags = [a.replace(" ", "_") for a in new_tags]  # 空格变下划线

    new_tags = remove_mutex(new_tags, tuple(sdt.mutex_tags))  # 去除mutex
    new_tags = [replace_duplicates(a, "\\\\", "\\") for a in new_tags]  # 去除重复斜杠

    if lite_mode:
        new_tags = remove_taboo_tags(new_tags, globals.trash_tags)
    else:
        new_tags = remove_taboo_tags(new_tags, sdt.gensettings.taboo_tags)  # 去除taboo
    new_tags = utils.remove_dupe(new_tags)  # 去重  # todo: 没去掉trash tag??
    return new_tags


def __gen_oneline(sdtools, tag_count: int, ) -> List[str]:
    """
    :param sdtools: class SDTools
    :param gs: 设置 (vital, end, taboo)
    :param tag_count:
    :return:
    """
    gs = sdtools.gensettings
    assert sdtools.tags_dict and sdtools.gensettings  # 不为空

    end_tags_len = len(gs.end_tags)
    new_tags = [utils.random_select(sdtools.tags_dict) for i in range(tag_count * 2)]  # 从weighted_dict随机生成2n个
    new_tags = list(dict.fromkeys(new_tags))  # 去重
    new_tags = remove_occurence_if_exists(gs.vital_tags + gs.end_tags, new_tags)  # 去除已存在的开头结尾tag

    new_tags = gs.vital_tags + new_tags  # 前部添加vital_tag
    if gs.accent_tags:  # 添加accent
        new_tags = new_tags + random.choices(gs.accent_tags, k=gs.accent_count)

    new_tags = clean_tags(sdtools, new_tags)  # 数据清理

    return new_tags[:tag_count - end_tags_len] + gs.end_tags  # 返回前n个

    # return ["1girl", "best quality", "by sks"]


def gen_prompt(sdtools, tag_count: int, line_count: int) -> List[str]:
    """
    :param tag_count: 每行几个tag
    :param line_count: 总共几行
    :param config_dict: 设置 (开头, 结尾, etc)
    :return:  生成的prompt list
    """
    prompt_list = []

    for i in range(line_count):
        tags_str = ", ".join(__gen_oneline(sdtools, tag_count))
        prompt_list.append(tags_str)

    return prompt_list


def get_txt_prompt(sdt, count: int) -> List[str]:
    """
    从sdt指定的文件目录读取[count]个txt里的prompt, 每行一格
    :param sdt: SDTools
    :param count: 生成n行
    :return:
    """
    tag_lines = sdt.txt_lines
    actual_lines = random.choices(tag_lines, k=count)
    actual_lines = [", ".join(clean_tags(sdt, line, lite_mode=True)) for line in actual_lines]

    return actual_lines
