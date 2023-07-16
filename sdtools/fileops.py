import json
import os
import collections
from typing import List, Dict

"""文件操作, 主要是getters
设置到全局应该用setters.py
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


if __name__ == '__main__':
    dir = "D:\Andrew\Pictures\Grabber\c123Eagle.OG"
    read_txt_files(dir)
