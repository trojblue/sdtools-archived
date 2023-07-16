import os

from tqdm import tqdm

from legacy.settings import *
from legacy.helpers import *
from sdtools.aug_text import process_text
from sdtools.fileops import *

def clean_folder(addr: str, prepend_txt:str=""):
    """
    清洗<addr>内的所有文本文档
    **注意会覆盖原文件, 最好先备份**
    """
    all_files = os.listdir(addr)
    txt_files = filter(lambda x: x[-4:] == '.txt', all_files)  # 文件夹下的所有txt文件
    counter = 0

    for i in tqdm(txt_files):
        path = addr + "\\" + i
        with open(path, 'rt') as fd:
            one_liner = ", ".join(fd.readlines())
            out_line = process_text(one_liner)  # 关键步骤

            out_line_tags = out_line.split(", ")
            if prepend_txt not in out_line_tags:
                out_line_tags = [prepend_txt] + out_line_tags

            out_line = ", ".join(out_line_tags)
            #
            # out_line_lst = out_line[-len(prepend_txt):]
            # if out_line_lst != prepend_txt:
            #     out_line += prepend_txt

        with open(path, 'w') as f:
            f.write(out_line)
        counter += 1

    print("已处理 %d个文本" % counter)


if __name__ == '__main__':
    addr = input("输入训练集地址: ")
    prepend_txt = "sks"
    backup_files(addr, '.txt')
    clean_folder(addr, prepend_txt)
