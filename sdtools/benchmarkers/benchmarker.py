class Benchmarker():

    def __init__(self, sdt):
        self.sdt = sdt

    def get_sampler(self):
        return "DDIM"

    def get_step(self):
        raise NotImplementedError

    def gen_benchmarks(self):
        raise NotImplementedError

    def get_bench_name(self, json):
        """根据samper. step, seed生成图片前缀的bench_name
        :param json: 当前的单个test
        """
        return "%s_step%s_seed_%d" \
               % (json["sampler_index"], json["steps"], json["seed"])


