import base64
import io
import json
import os
from datetime import datetime
from typing import List

import requests
from PIL import PngImagePlugin, Image

from sdtools.benchmarkers.b_fixed_prompt import BenchFixedPrompt
from sdtools.benchmarkers.b_random_minimum import BenchRandomMin

import time
from tqdm import tqdm

from sdtools.utils import mkdir_if_not_exist, curr_method_str

SAVE_PATH = "./out/"
BENCH_URL = "http://127.0.0.1:7860"

def run_benchmarks(sdt, benchmarks, name: str):
    """
    1. 生成requests json
    2. 发送requests json到webui
    3. 收集数据
    :param sdt: SDTools class
    :param benchmarks: Dict
    :param name: 文件夹名字
    """
    start_time = datetime.now().strftime("%y.%m.%d_%H%M")
    # model_name = requests.get(BENCH_URL + "/sdapi/v1/sd-models").json()
    folder_name = (start_time + "_" + name) + "/"
    cfg_name = "config_" + start_time + ".json"


    # 创建文件夹, 保存参数
    dir_route = os.path.join(SAVE_PATH, folder_name)  # /out/1111_1111_name/
    mkdir_if_not_exist(dir_route)
    with open(os.path.join(dir_route, cfg_name), 'w') as f:
        json.dump(benchmarks, f, indent=2)

    # 进度条
    total_steps = sum([i["benchmark_json"]["steps"] for i in benchmarks])
    print("test count: %d | total steps: %d" % (len(benchmarks), total_steps))
    time.sleep(0.5)
    pbar = tqdm(total=total_steps)

    # bench
    for b in benchmarks:
        curr_json = b["benchmark_json"]
        pbar.set_description("生成 [%s]" % b["benchmark_name"])

        url = BENCH_URL + "/sdapi/v1/txt2img"
        req = requests.post(url, json=curr_json)
        r = req.json()

        save_img(b, curr_json, dir_route, r)
        pbar.update(int(curr_json["steps"]))

    pbar.close()


def save_img(b, curr_json, dir_route, r):
    """b: benchmark
    r: response
    """
    png_num = 0
    for curr_img in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(curr_img.split(",", 1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + curr_img
        }
        response2 = requests.post(url=f'{BENCH_URL}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        info = response2.json().get("info")
        pnginfo.add_text("parameters", info)

        curr_time = datetime.now().strftime("%y.%m.%d_%H%M%S")
        png_name = "%s_%s_%s.png" % (b["benchmark_name"], png_num, curr_time)
        png_route = os.path.join(dir_route, png_name)

        # dir_route+"png/" + i["benchmark_name"] + "_seed" + str(curr_json["seed"])+"_"+i+".png"
        image.save(png_route, pnginfo=pnginfo)

        png_num += 1


def do_get_samplers() -> List[str]:
    """返回所有可用samplers"""
    samplers = requests.get(url=f'{BENCH_URL}/sdapi/v1/samplers').json()
    sampler_strings = [i["name"] for i in samplers]
    return sampler_strings



def do_random_benchmark(sdt, model_name):
    """
    1. 生成requests json
    2. 发送requests json到webui
    3. 收集数据
    :param sdt: SDTools class
    """
    bench = BenchRandomMin(sdt)
    benchmarks = bench.gen_benchmarks()
    name =  model_name+"_"+curr_method_str()
    run_benchmarks(sdt, benchmarks, name=name)

def do_fixed_prompt_bencmark(sdt, model_name):
    """prompt固定, 寻找alternative
    """
    bench = BenchFixedPrompt(sdt)
    benchmarks = bench.gen_benchmarks()
    name =  model_name+"_"+curr_method_str()
    run_benchmarks(sdt, benchmarks, name=name)


# 无法独立运行