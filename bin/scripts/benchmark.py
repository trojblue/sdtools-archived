import argparse
import base64
from io import BytesIO

from PIL import Image
from PIL import ImageDraw

import requests
import json


def parse_args(input_args=None):
    parser = argparse.ArgumentParser(description="Simple example of prompt_start Benchmark script.")
    parser.add_argument(
        "--benchmark_path",
        type=str,
        default=None,
        required=True,
        help="Path to benchmark json",
    )
    # parser.add_argument(
    #     "--SAVE_PATH",
    #     type=str,
    #     default=None,
    #     required=False,
    #     help="Path to save benchmark result",
    # )
    parser.add_argument(
        "--url",
        type=str,
        default="http://127.0.0.1:7860/",
        required=False,
        help="Target webui url",
    )
    parser.add_argument(
        "--expect_benchmark",
        type=str,
        default=None,
        required=False,
        help="Some benchmark you don't want to run use like --expect_benchmark 'nameA,nameB' see the benchmark.json"
    )
    parser.add_argument(
        "--sfw",
        default=False,
        action="store_true",
        help="Generate sfw only"
    )
    if input_args is not None:
        args = parser.parse_args(input_args)
    else:
        args = parser.parse_args()

    return args


def main(args):
    with open(args.benchmark_path, 'r', encoding='utf-8') as f:
        benchmark_json = json.loads(f.read())
    expect_str: str = args.expect_benchmark
    expect_list = []
    if expect_str != "" and expect_str is not None:
        expect_list = expect_str.split(",")
    img_list = []
    width_list = []
    height_list = []
    benchmark_name_list = []
    for i in benchmark_json["benchmark"]:
        if expect_list is not None and expect_str is not None:
            if i["benchmark_name"] in expect_list:
                continue
        if args.sfw:
            if i["benchmark_type"] == "nsfw":
                continue
        req = requests.post(args.url + "sdapi/v1/txt2img", json=i["benchmark_json"])
        response = json.loads(req.content)
        y_count = 0
        width = i["benchmark_json"]["width"]
        height = i["benchmark_json"]["height"]
        n_iter = i["benchmark_json"]["n_iter"]
        batch_size = i["benchmark_json"]["batch_size"]
        img = Image.new(size=(width, height * n_iter * batch_size), mode="RGB")
        for j in response["images"]:
            tmp_img = Image.open(BytesIO(base64.b64decode(j)))
            img.paste(tmp_img, (0, height * y_count))
            y_count += 1
        img.save(i["benchmark_name"] + ".jpg")
        img_list.append(img)
        width_list.append(width)
        height_list.append(height * y_count - 1)
        benchmark_name_list.append(i["benchmark_name"])
    sum_img = Image.new(size=(sum(width_list), max(height_list) + 100), mode="RGB")
    drawer = ImageDraw.Draw(sum_img)
    for i in range(0, img_list.__len__()):
        sum_img.paste(img_list[i], (sum(width_list[0:i]), 100))
        drawer.text(((sum(width_list[0:i]) + (width_list[i] / 2)), 50), benchmark_name_list[i], fill=(255, 255, 255))
    sum_img.save("sum.jpg")


if __name__ == "__main__":
    args = parse_args()
    main(args)
