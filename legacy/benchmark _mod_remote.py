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


def do_single_grid(checkpoint_name, benchmark_json: Dict, folder_name: str = None, gen_summary_img=True):
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

        try:
            req = requests.post(url + "/sdapi/v1/txt2img", json=curr_json, headers={'Accept-Encoding': 'identity'})
        except Exception as e:
            print(e)
            print("request失败: prompt= %s"%curr_json['prompt'])
            continue

        r = req.json()
        # todo: 检查r images是否存在

        png_num = 0
        for curr_img in [r['images'][0]]:   # 不知道是什么bug总之只保存一张图
            image = Image.open(io.BytesIO(base64.b64decode(curr_img.split(",", 1)[0])))

            png_payload = {
                "image": "data:image/png;base64," + curr_img
            }
            try:
                response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload, headers={'Accept-Encoding': 'identity'})
                pnginfo = PngImagePlugin.PngInfo()
                info = response2.json().get("info")
                pnginfo.add_text("parameters", info)
            except Exception as e:
                print("pnginfo失败: prompt= %s" % curr_json['prompt'])
                print(e)
                pnginfo = PngImagePlugin.PngInfo()
                pnginfo.add_text("parameters", curr_json['prompt']+"seed"+curr_json["seed"])

            curr_time =datetime.now().strftime("%y.%m.%d_%H%M%S")
                        # 采样 #seed #模型名
            png_route = "%s%s_seed%d_%s_%s_%s.png" % \
                        (dir_route, b["benchmark_name"], curr_json["seed"], checkpoint_name, png_num, curr_time)

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


def do_benchmark(model_name:str="NONAME"):
    """一次做多组测试
    doc: http://127.0.0.1:7860/docs

    """

    preset_DEBUG = {
        "folder_name": "debug",
        "sampler_list": "Euler, Euler mecha_tags, DDIM".split(", "),
        "step_list": [10, 15],
        "cfg_list": [7],
        "resolution": (512, 512),
        "prompt_list": [p_orange_white_miku]
    }

    preset_EVAL_SAMPLER = {
        "folder_name": "miko12f_orange_oversized",
        "sampler_list": "Euler, Euler mecha_tags, DDIM, DPM++ 2M Karras".split(", "),
        "step_list": [15, 20, 25, 31, 39, 52, 69, 120],
        "cfg_list": [7],
        "resolution": (1024, 768),
        "prompt_list": [p_orange_white_miku]
    }

    preset_STEP_CFG = {
        "folder_name": "miko12f_orange_oversized",
        "sampler_list": ["Euler mecha_tags"],
        "step_list": [i for i in range(16, 26)],
        "cfg_list": [6, 6.5, 7, 7.5, 8],
        "resolution": (1024, 768),
        "prompt_list": [p_orange_white_miku]
    }

    preset_EVAL_PROMPTS = {
        "folder_name": "miko12f_EVAL_PROMPTS",
        "sampler_list": "Euler, Euler mecha_tags, DDIM, DPM++ 2M Karras".split(", "),
        "step_list": [15, 20, 25, 31, 39, 52, 69, 120],
        "cfg_list": [7],
        "resolution": (1024, 768),
        "prompt_list": [p_white_drink_realistic, p_black_demon_girl, p_qipao]
    }

    random_prompt_list = generate_prompt_to_list(tag_count=47, line_count=100)
    # paste_list_to_clipboard(random_prompt_list)

    MODEL_NAME = model_name
    # todo: 记住上回名字

    #   ↓ CKE210: 略微不够
    # (960, 704)  (1024, 768)
    resolution_random = (960, 704)
    resolution_random_v = (704, 960)
    resolution_illust = (1024, 768)
    resolution_illust_verti = (768, 1024)
    resolution_illust_verti_colab = (960, 1280)


    # iterative samplers
    preset_FIXED_PROMPT = {
        "folder_name": MODEL_NAME + "_FIXED_PROMPTS",
        "sampler_list": ["DDIM", "DPM++ 2M Karras"],
        "step_list": [25, 31, 39, 52, 69, 85],
        "cfg_list": [6.5, 7, 7.5],
        "resolution": resolution_illust,
        "prompt_list": [p_green_space]
    }

    # non-iterative samplers
    preset_FIXED_PROMPT_NI = {
        "folder_name": MODEL_NAME + "_FIXED_PROMPTS_NI",
        "sampler_list": ["Euler mecha_tags", "Euler"],
        "step_list": [31, 39, 52],
        "cfg_list": [6.5, 7, 7.5],
        "resolution": resolution_illust,
        "prompt_list": [p_green_space]
    }

    preset_FAST_PROMPT = {
        "folder_name": MODEL_NAME + "_FAST_PROMPTS",
        "sampler_list": ["DDIM", "DPM++ 2M Karras", "Euler mecha_tags"],
        "step_list": [25, 42],
        "cfg_list": [6.5],
        "resolution": resolution_illust_verti,
        "prompt_list": random_prompt_list
    }  # 40 tag: ~150 token

    preset_COLAB_PROMPT = {
        "folder_name": MODEL_NAME + "_COLAB_PROMPTS",
        "sampler_list": ["DDIM", "DPM++ 2M Karras", "Euler mecha_tags"],
        "step_list": [25, 42],
        "cfg_list": [6.5],
        "resolution": resolution_illust_verti,
        "prompt_list": random_prompt_list
    }  # 40 tag: ~150 token

    for p in ([preset_COLAB_PROMPT]):
        bench_json = gen_tests(sampler_list=p["sampler_list"],
                               step_list=p["step_list"],
                               cfg_list=p["cfg_list"],
                               prompt_list=p["prompt_list"],
                               netagive=neg_longer_hands,              # 长NEG
                               resolution=p["resolution"],
                               )
        do_single_grid("CMA10hf3_mk12f_cl17_03_COLAB", bench_json, folder_name=p["folder_name"],
                       gen_summary_img=False)

    # do_debug_gen(preset_DEBUG)


def do_debug_gen(preset_DEBUG):
    p = preset_DEBUG
    # todo: prompt_list变为[(positive, negative)]
    # todo: 在同目录下生成log文件
    bench_json = gen_tests(sampler_list=p["sampler_list"],
                           step_list=p["step_list"],
                           cfg_list=p["cfg_list"],
                           prompt_list=p["prompt_list"],
                           netagive=neg_realistic,
                           resolution=p["resolution"],
                           seed_list=None
                           )
    do_single_grid("CMA10hf3_mk12f_cl17_03_COLAB", bench_json, folder_name=p["folder_name"],
                   gen_summary_img=False)


url = "https://b1c33de98f2b6e2a.gradio.app"
if __name__ == "__main__":
    # pyperclip.copy("doing benchmark")  # 复制到剪贴板, 去掉最后一个\n
    # spam = pyperclip.paste()
    do_benchmark("CMA10hf3_mk12f_cl17_03_COLAB")
