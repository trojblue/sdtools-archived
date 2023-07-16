# CorpusTools_SD

stable diffusion prompting/training related scripts

适配Automatic1111的stable diffusion webui

<p>

#### 自动化生成

`benchmark_mod.py`: 

- 通过API连接webui, 根据配置批量生成图片
- 用于模型评价, 或者配合随机prompt实现全自动色图
- 配置方式见 `do_benchmark()`

- 需要在webui启动项加上`--api`


最简使用例 (`benchmark_mod.py` → `do_benchmark()`):
```python
# 设置参数
preset_EVAL_SAMPLER = {
    "folder_name": "test_orange_oversized",
    "sampler_list": "Euler, Euler a, DDIM, DPM++ 2M Karras".split(", "),
    "step_list": [15, 20, 25, 31, 39, 52, 69, 120],
    "cfg_list": [7],
    "resolution": (1024, 768),
    "prompt_list": [p_orange_white_miku]
}

p = preset_EVAL_SAMPLER

# 生成json
bench_json = gen_tests(sampler_list=p["sampler_list"],
                       step_list=p["step_list"],
                       cfg_list=p["cfg_list"],
                       prompt_list=p["prompt_list"],
                       netagive=neg_realistic,
                       resolution=p["resolution"],
                       seed_list=None
                       )
# 连接到webui api
do_single_grid(bench_json, folder_name=p["folder_name"], gen_summary_img=False)
```


#### 生成随机prompt

`gen_prompts.py` 

- 根据训练集的txt随机生成prompt, 复制到剪贴板
- 配合webui的脚本"prompts from file or textbox"使用

```
vital tags: 一定会出现的tag, 写入质量词
accent tags: 列表里一定随机选择n个的tag, 写入自己的xp
taboo_tags: 避免出现的tag
mutex_tags: 互相冲突, 只能出现一个的tag
```


#### 处理数据集

`aug_text.py`: 清理txt格式的tag文件

`aug_image.py`: 

- 翻转图片(而不裁剪成正方形), 用于arb训练; 
- 复制txt到翻转后的图片旁边
- 随机打乱图片顺序
- 删除图片的EXIF / PNG chunk信息



#### 其他

**tags.json:**

根据输入类型, 自动处理mutex/mutable/coexist

- mutex: 只能存在一种, 比如`blue hair`和`blonde hair`会互相冲突
- mutable: 在指定元素中选择一定比例包含在prompt里
- coexist: 生成特定人物时必须包含要素, 比如初音要有蓝/绿头发

**settings**:

项目的设置都在这里, 具体见注释

