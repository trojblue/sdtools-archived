from gen_prompts import *
import os


def read_files(addr: str):  # 01: 所有文件读取操作
    global all_tags_list
    all_files = os.listdir(addr)
    txt_files = filter(lambda x: x[-4:] == '.txt', all_files)  # 文件夹下的所有txt文件

    all_tags = []

    for i in txt_files:
        path = addr + "\\" + i
        with open(path, 'rt') as fd:
            lines = fd.readlines()
            single_line_tags = ", ".join(lines).split(",")
            all_tags.append(single_line_tags)

    return all_tags


def get_OG_line_from_train(addr, count:int):
    tag_lines = read_files(addr)

    actual_lines = random.choices(tag_lines, k=count)
    actual_lines = [", ".join(clean_tags_lite(i)) for i in actual_lines]

    paste_list_to_clipboard(actual_lines)
    return actual_lines



if __name__ == '__main__':
    # 无输入得到50条原文prompt
    print("无输入得到50条原文prompt:")
    addr = "D:\Andrew\Pictures\Grabber\c123Eagle.OG"
    get_OG_line_from_train(addr, 50)