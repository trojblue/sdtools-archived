import os

import sdtools
import sdtools.config_gen
import sdtools.sdt
from sdtools.bench_settings import BenchSettings
from sdtools.config_bench import *
import sdtools.benchmark_remote as b_remote


def do_random_test():
    gs = sdtools.config_gen.main_settings
    bs = BenchSettings(preset_QUICK_SAMPLERS)
    src_dir = dst_dir ="D:\Andrew\Pictures\Grabber\c123Eagle.OG - 副本"
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

    b_remote.do_fixed_prompt_bencmark(sdt, model_name="d0c_nice_035")


    sdt.do_fixed_prompt_benchmark(model_name="mk11_last")


if __name__ == '__main__':
    do_fixed_prompt_test()