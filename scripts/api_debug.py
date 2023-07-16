import requests

import sdtools
from sdtools.config_gen import *
from sdtools import sdt
from sdtools.bench_settings import BenchSettings
from sdtools.benchmark import *
from sdtools.benchmarkers.b_fixed_prompt import BenchFixedPrompt
from sdtools.benchmarkers.b_random_minimum import BenchRandomMin
from sdtools.utils import curr_method_str

from sdtools.config_bench import *
from sdtools.globals import *

api_settings = {
    "samplers": "Euler, DDIM",
    "step_list": [5],
    "cfg_list": [6.5, 7.5],
    "tag_count": 30,
    "line_count": 1,
    "negative": "",
    "resolution": (256, 256),
    "prompt_list": ["1girl, best quality, by sks"],
    "seed": -1
}



def run_benchmarks_private(sdt, benchmarks, name: str):
    """
    1. 生成requests json
    2. 发送requests json到webui
    3. 收集数据
    :param sdt: SDTools class
    :param benchmarks: Dict
    :param name: 文件夹名字
    """
    # bench
    start_time = datetime.now().strftime("%y.%m.%d_%H%M")
    folder_name = (start_time + "_" + name) + "/"
    dir_route = os.path.join(SAVE_PATH, folder_name)

    for b in benchmarks:
        curr_json = b["benchmark_json"]


        u_models = RMOTE + "/sdapi/v1/sd-models"
        r_model = requests.get(u_models)
        r_model2 = r_model.json()

        u_cfg = RMOTE + "/config"
        r_cfg= requests.get(u_cfg)
        r_cfg2 = r_cfg.json()

        u_stats = RMOTE + "/queue/status"
        r_stats = requests.get(u_stats)
        r_stats2 = r_stats.json()

        url1 = RMOTE + "/sdapi/v1/txt2img"
        req = requests.post(url1, json=curr_json)
        r = req.json()

        url2 = RMOTE + "/sdapi/v1/txt2img"
        req2 = requests.post(url2, json=curr_json)
        r2 = req2.json()

        save_img(b, curr_json, dir_route, r)


# 注意有端口号, 没有斜杠
# RMOTE = "https://c84a-3-136-172-40.ngrok.io"
RMOTE = "https://37f76f4a05f9219d.gradio.app"
# RMOTE = "http://127.0.0.1:7860"

LOCAL = "http://127.0.0.1:7860"


def do_api():
    model_name = "bench_api"
    bs = BenchSettings(api_settings)

    src_dir = dst_dir ="D:\Andrew\Pictures\Grabber\combine1\chi4"
    sdt = sdtools.sdt.SDTools(src_dir=src_dir, dst_dir=dst_dir, gs=main_settings, bs=bs)
    benchmarks = BenchFixedPrompt(sdt).gen_benchmarks()

    name =  model_name+"_"+curr_method_str()

    run_benchmarks_private(sdt, benchmarks, name=name)

    print("D")


if __name__ == '__main__':
    do_api()