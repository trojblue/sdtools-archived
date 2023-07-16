from typing import *
import pyperclip

def remove_dupe(the_list: List) -> List:
    """输入list, 返回去重版"""
    return list(dict.fromkeys(the_list))


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

def paste_list_to_clipboard(prompt_list):
    clipboard = ""
    for p in prompt_list:
        clipboard += p + "\n"

    pyperclip.copy(clipboard[:-1])  # 复制到剪贴板, 去掉最后一个\n
    spam = pyperclip.paste()
    print("已复制%d行到剪贴板" % len(prompt_list))