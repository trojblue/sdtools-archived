import copy
import random

from sdtools.benchmarkers.benchmarker import Benchmarker
import sdtools.benchmark
from sdtools.config_bench import barebone_test
from sdtools.utils import get_random_seed


class BenchFixedPrompt(Benchmarker):

    def __init__(self, sdt):
        """
        :param sdt: SDTools class
        固定prompt, 用尽可能多的sampler测试; step会响应变高
        如果seed不是-1, 则使用seed
        """
        super().__init__(sdt)

    def gen_benchmarks(self):
        """
        """
        sdt, bs = self.sdt, self.sdt.benchsettings
        test_list = []
        line_count, tag_count = bs.line_count[0], bs.tag_count[0]
        negative = bs.negative[0]
        # todo: ↑ ugly

        # 顺序: prompt -> seed -> cfg -> step -> sampler
        for prompt in bs.prompt_list:
            for cfg in bs.cfg_list:
                for step in bs.step_list:
                    for sampler in bs.sampler_list:

                        curr_test = copy.deepcopy(barebone_test)
                        json = curr_test["benchmark_json"]
                        json["prompt"] = prompt
                        json["cfg_scale"] = cfg
                        json["steps"] = step
                        json["sampler_index"] = sampler
                        json["negative_prompt"] = negative
                        json["seed"] = bs.seed if bs.seed != -1 else get_random_seed()

                        # 存在图片文件最前面的前缀
                        curr_test["benchmark_name"] = self.get_bench_name(json)

                        curr_test["benchmark_json"] = json
                        test_list.append(curr_test)

        return test_list



