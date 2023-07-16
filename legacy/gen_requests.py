import copy
import random
from typing import List, Dict, Tuple
from settings import *
from gen_prompts import generate_prompt_to_list


def get_barebone_test():
    """返回默认测试; 会被之后的覆盖"""
    # todo: 此处性能瓶颈
    curr_prompt = generate_prompt_to_list(tag_count=30, line_count=1)
    barebone_test = {
        "benchmark_name": "default",
        "benchmark_type": "sfw",
        "benchmark_json": {
            "prompt": curr_prompt[0],
            "seed": -1,
            "batch_size": 1,
            "n_iter": 2,
            "steps": 20,
            "cfg_scale": 7,
            "width": 768,
            "height": 960,
            "negative_prompt": MY_NEG,
            "sampler_index": "Euler a"
        }
    }
    return barebone_test

def get_random_seed():
    return random.randint(0, 4294967295)

def list_to_test(test_list) -> Dict:
    return {"benchmark": test_list}


def gen_tests_primal(sampler_list, step_list,
                     resolution: Tuple = None,
                     prompt: str = None,
                     netagive:str=None,
                     cfg:int=None,
                     seed_list=None) -> List:
    """生成step vs sampler的训练List (不是字典!)

    seed_list: 为每个seed分别生成图片 (等于individual batch count)
    """
    if seed_list is None:
        seed_list = [-1]

    test_list = []

    for seed in seed_list:
        for steps in step_list:
            for sampler in sampler_list:
                curr_test = copy.deepcopy(get_barebone_test())    #单个test可以包含多个sample
                curr_json = curr_test["benchmark_json"]
                curr_json["sampler_index"] = sampler
                curr_json["steps"] = steps

                # 如果没有指定seed, 每个测试用单独seed; 否则所有测试用相同seed
                curr_json["seed"] = seed if seed != -1 else get_random_seed()
                if netagive:
                    curr_json["negative_prompt"] = netagive
                if resolution:
                    curr_json["width"] = resolution[0]
                    curr_json["height"] = resolution[1]
                if prompt:
                    curr_json["prompt"] = prompt
                if cfg:
                    curr_json["cfg_scale"] = cfg

                curr_test["benchmark_name"] = sampler + "_step" + str(steps) + "_cfg" + str(curr_json["cfg_scale"])
                test_list.append(curr_test)

    return test_list


def gen_full_sampler_step_tests() -> Dict:
    sampler_index_list = "Euler, Euler a, DDIM, DPM++ 2M Karras".split(", ")
    steps_list = [20, 31, 39, 52, 69, 120]
    # steps_list = "20, 31, 39, 50, 69".split(", ")
    cfg_list = [6.5, 7, 7.5, 8]

    resolution = (1024, 768)

    custom_prompt = "a clean painting of 1girl, aqua_eyes, aqua_hair, black_gloves, gloves, hatsune_miku, headphones, headset, holding, ((holding_staff)), jacket, close_up, hand_focus, (oversized_object, machine), orange decorations, racing, falling, pilot goggles, long_hair, depth of field, looking_at_viewer, simple_background, solo, staff, thighhighs, twintails, very_long_hair, white_background, white_jacket"
    sample_step_tests = gen_tests_primal(sampler_index_list, steps_list,
                                         resolution=resolution,
                                         prompt=custom_prompt)
    return list_to_test(sample_step_tests)


def gen_tests(sampler_list:List[str],
              step_list: List[int],
              cfg_list:List[int],
              prompt_list: List[str],
              netagive: str,
              resolution: Tuple,
              seed_list:List[str]= None
              ) -> Dict:
    """生成的的All in one function
    bench_json = gen_tests(sampler_list=["DPM++ 2M Karras"],
                           step_list=[i for i in range(16, 26)],
                           cfg_list=[6.5, 7, 7.5],
                           prompt_list=[prompt]
                           resolution=(1024, 768),
                           )
    """
    prompt_list = [None] if not prompt_list else prompt_list

    whole_list = []

    for prompt in prompt_list:
        for curr_cfg in cfg_list:
            new_list = gen_tests_primal(sampler_list, step_list, resolution,
                                        prompt, netagive, curr_cfg, seed_list)
            whole_list += new_list

    return list_to_test(whole_list)



if __name__ == '__main__':
    pass
