from typing import Dict


class BenchSettings():
    """
    包含: sampler, step, cfg, prompt, neg, res, seed

    """

    def __init__(self, preset_dict: Dict):
        """
        :param preset_dict: 见下面的例子

        line count: 模式随机时为生成测试的数量, 不是真随机时line_count无效
        seed: -1等于生成prompt时生成seed,固定值时锁定seed
        """

        p = preset_dict
        preset_name = [i for i, a in locals().items() if a == p][0]  # preset字典的变量名

        self.name = preset_name
        self.sampler_list = p["samplers"].split(", ")
        self.step_list = p["step_list"]
        self.cfg_list = p["cfg_list"]
        self.tag_count = p["tag_count"],
        self.line_count = p["line_count"],
        self.negative = p["negative"],
        self.resolution = p["resolution"],
        self.prompt_list = p["prompt_list"]
        self.seed = p["seed"]