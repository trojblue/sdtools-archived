import base64
import io
import math
import time
from datetime import datetime

import requests
from PIL import Image, PngImagePlugin
from PIL import ImageDraw, ImageFont
from tqdm import tqdm

from gen_requests import *
from gen_prompts import *

bench_json = "bin/benchmark.json"
SAVE_PATH = "../out/"
url = "http://127.0.0.1:7860"


def image_grid(n_rows: int, imgs: List, batch_size=1, rows=None):
    """imgs: 所有图片的list
    """
    if rows is None:
        if n_rows > 0:
            rows = n_rows
        elif n_rows == 0:
            rows = batch_size
        # elif opts.grid_prevent_empty_spots:
        #     rows = math.floor(math.sqrt(len(imgs)))
        #     while len(imgs) % rows != 0:
        #         rows -= 1
        else:
            rows = math.sqrt(len(imgs))
            rows = round(rows)

    cols = math.ceil(len(imgs) / rows)  # 列数= 总图片/行数

    w, h = imgs[0].size
    grid = Image.new('RGB', size=(cols * w, rows * h), color='black')

    for i, img in enumerate(imgs):
        grid.paste(img, box=(i % cols * w, i // cols * h))

    return grid


def mkdir_if_not_exit(path):
    try:
        os.makedirs(path)
    except Exception:
        pass


def do_single_grid(benchmark_json: Dict, folder_name: str = None, gen_summary_img=True):
    """从Json配置单生成单张合成图
    """
    img_list = []
    width_list = []
    height_list = []
    benchmark_name_list = []
    start_time = datetime.now().strftime("%y.%m.%d_%H%M")
    new_folder_name = (start_time if not folder_name else start_time + "_" + folder_name) + "/"  # 1111_1111_name/

    dir_route = SAVE_PATH + new_folder_name  # /out/1111_1111_name/
    mkdir_if_not_exit(dir_route)

    cfg_filename = "config_"+datetime.now().strftime("%y.%m.%d_%H%M")+".json"
    with open(dir_route + cfg_filename, 'w') as f:
        json.dump(benchmark_json, f, indent=2)

    total_steps = sum([i["benchmark_json"]["steps"] for i in benchmark_json["benchmark"]])
    print("test count: %d | total steps: %d" % (len(benchmark_json["benchmark"]), total_steps))
    time.sleep(0.5)

    pbar = tqdm(total=total_steps)

    for b in benchmark_json["benchmark"]:
        curr_json = b["benchmark_json"]
        pbar.set_description("生成 [%s]" % b["benchmark_name"])

        req = requests.post(url + "/sdapi/v1/txt2img", json=curr_json)

        r = req.json()
        # todo: 检查r images是否存在

        png_num = 0
        for curr_img in r['images']:
            image = Image.open(io.BytesIO(base64.b64decode(curr_img.split(",", 1)[0])))

            png_payload = {
                "image": "data:image/png;base64," + curr_img
            }
            response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

            pnginfo = PngImagePlugin.PngInfo()
            info = response2.json().get("info")
            pnginfo.add_text("parameters", info)

            curr_time =datetime.now().strftime("%y.%m.%d_%H%M%S")
            png_route = "%s%s_seed_%d_%s_%s.png" % \
                        (dir_route, b["benchmark_name"], curr_json["seed"], png_num, curr_time)

            # dir_route+"png/" + i["benchmark_name"] + "_seed" + str(curr_json["seed"])+"_"+i+".png"
            image.save(png_route, pnginfo=pnginfo)

            png_num += 1


        pbar.update(int(curr_json["steps"]))

    pbar.close()

    if gen_summary_img:
        sum_img = Image.new(size=(sum(width_list), max(height_list) + 100), mode="RGB")
        drawer = ImageDraw.Draw(sum_img)
        font_path = "C:\Windows\Fonts\JetBrains Mono\JetBrainsMono-MediumItalic.ttf"
        font = ImageFont.truetype(font_path, 30)

        for b in range(0, img_list.__len__()):
            sum_img.paste(img_list[b], (sum(width_list[0:b]), 100))
            drawer.text(((sum(width_list[0:b]) + (width_list[b] / 2)), 50), benchmark_name_list[b],
                        fill=(255, 255, 255), font=font, anchor="mm")
        sum_img.save(dir_route + "sum.jpg")


# class PromptSettings():
#     def __init__(self, sampler_list, step_list, cfg_list, resolution, prompt_list):
#         pass


def do_test(p):
    """p: preset -> config_gen.py
    """
    bench_json = gen_tests(sampler_list=p["sampler_list"],
                           step_list=p["step_list"],
                           cfg_list=p["cfg_list"],
                           prompt_list=p["prompt_list"],
                           netagive=neg_realistic,  # 长NEG
                           resolution=p["resolution"],
                           )
    do_single_grid(bench_json, folder_name=p["folder_name"],
                   gen_summary_img=False)


def do_benchmark(model_name:str="NONAME"):
    """一次做多组测试
    doc: http://127.0.0.1:7860/docs

    """

    random_prompt_list = generate_prompt_to_list(tag_count=30, line_count=25)
    paste_list_to_clipboard(random_prompt_list)

    MODEL_NAME = model_name
    # todo: 记住上回名字

    #   ↓ CKE210: 略微不够
    # (960, 704)  (1024, 768)
    resolution_random = (960, 704)
    resolution_random_v = (704, 960)
    resolution_illust = (1024, 768)
    resolution_illust_verti = (768, 1024)


    # DPM++ 2M Karras
    preset_RANDOM_PROMPT_DPMPP2MK = {
        "folder_name": MODEL_NAME + "_RANDOM_PROMPT",
        "sampler_list": ["DPM++ 2M Karras"],
        "step_list": [15, 20, 25, 31, 39, 52],
        "cfg_list": [6.5, 7],
        "resolution": resolution_random,
        "prompt_list": random_prompt_list
    }

    # iterative samplers
    preset_FIXED_PROMPT = {
        "folder_name": MODEL_NAME + "_FIXED_PROMPTS",
        "sampler_list": ["DDIM", "DPM++ 2M Karras", "DPM++ 2S a Karras"],
        "step_list": [25, 31, 39, 52, 69, 85],
        "cfg_list": [6.5],
        "resolution": resolution_random,
        "prompt_list": [p_cake]
    }

    # non-iterative samplers
    preset_FIXED_PROMPT_LESS = {
        "folder_name": MODEL_NAME + "_FIXED_PROMPT_LESS",
        "sampler_list": ["Euler a", "Euler", "Heun", "DPM++ SDE Karras"],
        "step_list": [31, 39, 52],
        "cfg_list": [6.5],
        "resolution": resolution_random,
        "prompt_list": [p_cake]
    }

    preset_FAST_PROMPT = {
        "folder_name": MODEL_NAME + "_FAST_PROMPTS",
        "sampler_list": ["DDIM", "DPM++ 2M Karras", "Euler a"],
        "step_list": [25, 42],
        "cfg_list": [6.5],
        "resolution": resolution_illust,
        "prompt_list": random_prompt_list
    }  # 40 tag: ~150 token

    preset_VERY_FAST_PROMPT = {
        "folder_name": MODEL_NAME + "_VERY_FAST_PROMPTS",
        "sampler_list": ["DDIM", "DPM++ 2M Karras", "Euler a", "Heun"],
        "step_list": [25, 29],
        "cfg_list": [6.5],
        "resolution": resolution_illust,
        "prompt_list": random_prompt_list
    }  # 40 tag: ~150 token

    for p in ([preset_EVAL_MODEL_RANDOM_longer]):

    # for p in ([preset_FIXED_PROMPT, preset_FIXED_PROMPT_NI]):
        do_test(p)

if __name__ == "__main__":
    # pyperclip.copy("doing benchmark")  # 复制到剪贴板, 去掉最后一个\n
    # spam = pyperclip.paste()
    do_benchmark("d0c_nice")
