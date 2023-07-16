import os

import sdtools
import sdtools.config_gen
import sdtools.sdt
from sdtools.benchmark import run_benchmarks
from sdtools.config_gen import *
from sdtools.prompt_settings import PromptSettings
from sdtools.prompts import get_txt_prompt
from sdtools.utils import *

from sdtools.bench_settings import BenchSettings
from sdtools.config_bench import *



def gen_prompt(tag_count, line_count, gs):

    src_dir = "D:\Andrew\Pictures\==train\\aesthetics_768_flipped"
    sdt = sdtools.sdt.SDTools(src_dir=src_dir, gs=gs)

    line = sdt.gen_prompt(tag_count=tag_count, line_count=line_count)
    line2 = sdt.get_txt_prompt(line_count=5)

    paste_list_to_clipboard(line)

    # bs = BenchSettings()


def image_aug():
    # 只能原地覆写, 运行前先手动保存一份备份
    src_dir = dst_dir ="D:\Andrew\Pictures\Grabber\c123Eagle.OG - 副本"
    sdt = sdtools.sdt.SDTools(src_dir=src_dir, dst_dir=dst_dir, gs=None)

    # 复制文件夹prompt到剪贴板
    # sdt.do_get_prompts()

    # 去除metadatam, 覆盖原文件(不添加suffix)
    sdt.do_remove_info(add_suffix = False, new_meta="")

    # 创建翻转
    sdt.do_flip()

    # 打乱图片
    sdt.do_shuffle()

def do_random_test():
    bench_settings = PromptSettings(
        start_word="(best quality:1.3), ",
        vital_tags="1girl",
        end_tags="original, highres",
        taboo_tags=longer_taboo_tags
    )

    # 每行会根据上面的bench_settings生成独特prompt
    gs = bench_settings
    bs = BenchSettings(preset_QUICKER_SAMPLERS)
    src_dir = dst_dir ="D:\Andrew\Pictures\==train\\niko.768.arb.shuffle2"
    sdt = sdtools.sdt.SDTools(src_dir=src_dir, dst_dir=dst_dir, gs=gs, bs=bs)

    sdt.do_random_benchmark()



def do_debug():
    gs = sdtools.config_gen.main_settings
    p = preset_QUICK_SAMPLERS
    p["resolution"] = (256, 256)
    bs = BenchSettings(p)
    src_dir = dst_dir ="D:\Andrew\Pictures\==train\PAST\c123Eagle.OG"
    sdt = sdtools.sdt.SDTools(src_dir=src_dir, dst_dir=dst_dir, gs=gs, bs=bs)

    sdt.do_random_benchmark()


def do_fixed_prompt_test():
    gs = sdtools.config_gen.intricate_settings
    bs = BenchSettings(preset_QUICK_SAMPLERS)
    bs.prompt_list=["(best quality:1.3), (masterpiece:0.5), (close-up:0.3), by sks,  (detailed:0.3), 1girl, (intricate:0.6), grey eyes, 1girl, bikini, hair between eyes, blue eyes, long hair, breasts, white dress, crying, close-up, yuge\(mkmk\), aqua ribbon, sitting, outstretched hand, frills, bow, halo, fish, green hair, monitor, frilled apron, facing away, anchor, :t, shoes, very long hair, blue nails, fork, bandaid, hexagon, carrying, rolua, blue flower, skirt, neckerchief, hair ornament, neco, original, highres"]
    bs.resolution=resolution_random
    # bs.seed=3364944276

    src_dir = dst_dir ="D:\Andrew\Pictures\Grabber\c123Eagle.OG - 副本"
    sdt = sdtools.sdt.SDTools(src_dir=src_dir, dst_dir=dst_dir, gs=gs, bs=bs)

    for i in range (99):
        sdt.do_fixed_prompt_benchmark(model_name="edc30110")


def do_get_txt_prompt():
    src_dir = "D:\Andrew\Pictures\Grabber\maimuro"
    sdt = sdtools.sdt.SDTools(src_dir=src_dir, gs=None)
    p_list = get_txt_prompt(sdt)
    paste_list_to_clipboard(p_list)



if __name__ == '__main__':
    do_random_test()


    pass




