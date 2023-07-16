from typing import List

from sdtools import fileops
import sdtools.prompts
import sdtools.benchmark
import inspect

from sdtools.benchmarkers.b_random_minimum import BenchRandomMin

import sdtools.benchmark

from sdtools.benchmark import BenchSettings
from sdtools.config_gen import PromptSettings

import sdtools.aug_image as aug_i
from sdtools.utils import curr_method_str


class SDTools():
    def __init__(self, src_dir=None, dst_dir=None, tagjson=None, gs: PromptSettings = None, bs: BenchSettings = None):
        """
        :param src_dir: augment / 生成prompt的地址
        :param tagjson: 带有tag信息的json文件
        :param gs: genSettings
        """
        self.src_dir = src_dir
        self.dst_dir = dst_dir
        self.tagjson = tagjson
        self.gensettings = gs
        self.benchsettings = bs
        # 设置self
        self.init_vars()
        pass

    def init_vars(self):
        # 初始化二级参数
        tagjson_dict = fileops.get_mutex_mutable_from_json(self.tagjson)
        tags_dict, txt_lines = fileops.read_txt_files(self.src_dir)
        self.mutex_tags = tagjson_dict["mutex"] if "mutex" in tagjson_dict else []
        self.mutable_tags = ["mutable"] if "mutable" in tagjson_dict else []
        self.tags_dict = tags_dict  # 训练集词频
        self.txt_lines = txt_lines  # 训练集原文

    # ================ BENCHMARK ====================

    def gen_prompt(self, tag_count: int, line_count: int) -> List[str]:
        """见prompts的doc
        """
        return sdtools.prompts.gen_prompt(self, tag_count, line_count)

    def get_txt_prompt(self, line_count: int) -> List[str]:
        """见prompts的doc
        """
        return sdtools.prompts.get_txt_prompt(self, line_count)

    def do_random_benchmark(self, model_name=""):
        """见prompts的doc
        """
        sdtools.benchmark.do_random_benchmark(self, model_name)

    def do_fixed_prompt_benchmark(self, model_name=""):
        """见prompts的doc
        """
        sdtools.benchmark.do_fixed_prompt_bencmark(self, model_name)

    # =============== IMAGE AUGMENTATION ==============

    def do_remove_info(self, add_suffix=True,
                       new_meta="upscaled by Topaz Gigapixel AI"):
        """
        去除src_dir里图片的metadata, 复制到dst_dir
        :param add_suffix: 是否在文件里加入_cleaned后缀, 准备覆盖原文件时用False
        :param new_meta: 去除水印后填入的新水印
        """
        aug_i.do_remove_info(self.src_dir, self.dst_dir, add_suffix, new_meta)

    def do_get_prompts(self):
        """复制src_dir里所有图片正面tag, 输出到剪贴板
        """
        aug_i.do_get_prompts(self.src_dir)

    def do_flip(self):
        """在target_dir创建src_dir图片的翻转版, 并复制txt到旁边
        """
        aug_i.do_flip(self.src_dir, self.dst_dir)

    def do_shuffle(self):
        """打乱src_dir数据集顺序, 输出到target_dir
        """
        aug_i.do_shuffle(self.src_dir, self.dst_dir)
