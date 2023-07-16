from typing import List, Tuple, Dict
from sdtools.globals import *
from sdtools.utils import get_random_seed

resolution_random = (960, 704)
resolution_random_v = (704, 960)
resolution_illust = (1024, 768)
resolution_illust_verti = (768, 1024)
resolution_random_smaller = (832, 640)
resolution_random_smaller_v = (640, 832)

# ========= BENCHMARK SETTINGS ============
bench_json = "bin/benchmark.json"

# =========== presets ============

# 之前一直默认的随机词条是30个
preset_QUICK_SAMPLERS = {
    "samplers": "Euler, Euler a, DDIM, DPM++ 2M Karras, DPM++ 2S a Karras, DPM++ SDE Karras, Heun",
    "step_list": [19, 25, 31, 37, 42, 65],
    "cfg_list": [6.5],
    "tag_count": 30,
    "line_count": 40,
    "negative": neg_realistic,
    "resolution": resolution_random,
    "prompt_list": [],
    "seed": -1
}

preset_EVERY_SAMPLER = {
    "samplers": "Euler, Euler a, DDIM, DPM++ 2M Karras, DPM++ 2S a Karras, DPM++ SDE Karras, Heun, ",
    "step_list": [19, 25, 31],
    "cfg_list": [6.5],
    "tag_count": 30,
    "line_count": 40,
    "negative": neg_realistic,
    "resolution": resolution_random,
    "prompt_list": [],
    "seed": -1
}


# 此处改小了
preset_EVAL_PROMPT = {
    "samplers": "Euler, Euler a, DDIM, DPM++ 2M Karras, DPM++ 2S a Karras, DPM++ SDE Karras, Heun",
    "step_list": [23, 25, 27, 31],
    "cfg_list": [6.5],
    "tag_count": 30,
    "line_count": 40,
    "negative": neg_realistic,
    "resolution": resolution_random,
    "prompt_list": [],
    "seed": -1
}

# debug
preset_random_debug = {
    "samplers": "Euler, Euler a, DDIM, DPM++ 2M Karras, DPM++ 2S a Karras, DPM++ SDE Karras, Heun",
    "step_list": [10, 15],
    "cfg_list": [6.5],
    "tag_count": 30,
    "line_count": 40,
    "negative": neg_realistic,
    "resolution": resolution_random,
    "prompt_list": [],
    "seed": -1
}

# ===============一般不要改的设置 =========

barebone_test = {
    "benchmark_name": "default",
    "benchmark_type": "sfw",
    "benchmark_json": {
        "prompt": "1girl",
        "seed": -1,
        "batch_size": 1,
        "n_iter": 2,
        "steps": 25,
        "cfg_scale": 7,
        "width": 768,
        "height": 960,
        "negative_prompt": "",
        "sampler_index": "Euler a"
    }
}
