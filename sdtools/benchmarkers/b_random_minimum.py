import copy
import random

from sdtools.benchmarkers.benchmarker import Benchmarker

import sdtools.benchmark

from sdtools.config_bench import barebone_test
from sdtools.utils import get_random_seed


class BenchRandomMin(Benchmarker):

    def __init__(self, sdt):
        """
        :param sdt: SDTools class
        :param bs: BenchSettings
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

        for i in range (line_count):
            curr_test = copy.deepcopy(barebone_test)
            json = curr_test["benchmark_json"]
            # 随机prompt
            json["prompt"] = sdt.gen_prompt(tag_count=tag_count, line_count=1)[0]

            # 随机sampler
            json["sampler_index"] = random.choice(bs.sampler_list)
            json["steps"] = random.choice(bs.step_list)
            json["cfg_scale"] = random.choice(bs.cfg_list)
            json["negative_prompt"] = negative
            json["seed"] = get_random_seed()

            # 存在图片文件最前面的前缀
            curr_test["benchmark_name"] = self.get_bench_name(json)

            curr_test["benchmark_json"] = json
            test_list.append(curr_test)

        return test_list



