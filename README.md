# SDTools

stable diffusion prompting/training related scripts

适配Automatic1111的stable diffusion webui

<p>


**V2: 重新变成python package的形式**



## Class
`SDTools` (sdt): 核心class, 包含功能所需的各项数据

`GenSettings` (gs): 生成输入词的参数class

`BenchSettings` (bs): 生成API测试的参数class

`tags.json`: 自定义词语包含关系, 见例子


## issues:

`create_inverse_trainset`: only supports jpg & png file




## 安装
一行版:
```bash
pip install git+https://github.com/trojblue/sdtools.git#egg=sdtools
```
手动安装:
```bash
git clone https://github.com/trojblue/sdtools
cd sdtools
python3 setup.py install
```
卸载sdtools & 安装指定版本:
```bash
pip uninstall sdtools
pip install git+https://github.com/trojblue/sdtools.git@v2#egg=sdtools sdtools
```


## 功能

**处理训练集:** 清除metadata/翻转, 支持多线程
```python
from sdtools.sdt import SDTools

# 只能原地覆写, 运行前先手动保存一份备份
src_dir = dst_dir ="D:\Andrew\Pictures\Grabber\c123Eagle.OG - 副本"
sdt = SDTools(src_dir=src_dir, dst_dir=dst_dir, gs=None)

# 复制文件夹所有txt里的prompt到剪贴板
# sdt.do_get_prompts()

# 去除metadatam, 覆盖原文件(即不添加suffix)
sdt.do_remove_info(add_suffix = False, new_meta="")

sdt.do_flip()       # 创建翻转图片
sdt.do_shuffle()    # 打乱顺序
```

**生成随机输入:**

```python
from sdtools import sdt
from sdtools.config_gen import main_settings

src_dir = "D:\Andrew\Pictures\Grabber\c123Eagle.OG"
sdt = sdt.SDTools(src_dir=src_dir, gs=main_settings)
line = sdt.gen_prompt(tag_count=35, line_count=2)
```

**benchmark:** 随机词模式

```python
import sdtools.config_gen, sdtools.sdt
from sdtools.bench_settings import BenchSettings
from sdtools.config_bench import preset_QUICK_SAMPLERS

gs = sdtools.config_gen.main_settings
bs = BenchSettings(preset_QUICK_SAMPLERS)
src_dir = dst_dir = "D:\Andrew\Pictures\Grabber\c123Eagle.OG - 副本"
sdt = sdtools.sdt.SDTools(src_dir=src_dir, dst_dir=dst_dir, gs=gs, bs=bs)

sdt.do_random_benchmark()
```


说明见`/sdtools/sdt.py`的method注释, 比如说:

```python
def do_remove_info(self, low_profile=True):
    """去除src_dir里图片的metadata, 复制到dst_dir
    """
    aug_i.do_replace_info(self.src_dir, self.dst_dir, low_profile)


def do_get_prompts(self):
    """复制src_dir里所有图片正面tag, 输出到剪贴板
    """
    aug_i.do_get_prompts(self.src_dir)


def do_flip(self):
    """在target_dir创建src_dir图片的翻转版, 并复制txt到旁边
    """
    aug_i.do_flip(self.src_dir, self.dst_dir)


def do_shuffle(self):
    """打乱src_dir数据集顺序, 输出到target_dir
    """
    aug_i.do_shuffle(self.src_dir, self.dst_dir)
```

