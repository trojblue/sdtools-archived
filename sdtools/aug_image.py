import os
import random
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import *

import PIL.ExifTags
import pyperclip
from PIL.JpegImagePlugin import JpegImageFile
from PIL.PngImagePlugin import PngImageFile, PngInfo
from PIL.WebPImagePlugin import WebPImageFile

from cv2 import cv2
from sdtools.utils import get_image_files

from PIL import Image, ImageOps, ImageFile


from tqdm import tqdm

from sdtools.utils import mkdir_if_not_exist, move_images




def get_image_files(src_dir: str):
    return [f for f in os.listdir(src_dir.lower()) if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.webp')]



def flip_all_imgs(src_dir, target_dir):
    """翻转src_dir的图片, 复制到target_dir
    """
    mkdir_if_not_exist(target_dir)
    image_files = get_image_files(src_dir)
    n_imgs = len(image_files)

    # 多线程, 并发
    # Process the images using ThreadPoolExecutor
    with tqdm(total=n_imgs, desc="flip images: ") as pbar:
        with ThreadPoolExecutor() as executor:
            # Submit a task for each image file to be processed by a thread
            tasks = [executor.submit(
                flip_single_image, src_dir, target_dir, filename)
                for filename in image_files]

            # Update the progress bar as tasks are completed
            for task in tasks:
                task.add_done_callback(lambda _: pbar.update())

            # Wait for all tasks to complete
            for task in tasks:
                task.result()

    # 单线程版本
    # for i in image_files:
    #     flip_single_image(src_dir, target_dir, i)

    print("%d flipped images saved to %s" % (len(image_files), target_dir))


def flip_single_image(src_dir, target_dir, filename):
    """翻转单张图片"""
    filepath = os.path.join(src_dir, filename)
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    im = Image.open(filepath)
    im_flip = ImageOps.flip(im)
    
    # img = cv2.imread(filepath)
    # flippedimage = cv2.flip(img, 1)  # horizontal
    new_name = "flip_" + filename
    new_path=os.path.join(target_dir, new_name)
    im_flip.save(new_path, quality=95)


    # cv2.imwrite(new_path, flippedimage)


def copy_all_txts(src_dir, target_dir):
    """读取src_dir内的txt文件, 复制到target, 并在target创建带_flip后缀的同内容文件
    """
    mkdir_if_not_exist(target_dir)
    all_files = os.listdir(src_dir)
    txt_files = filter(lambda x: x[-4:] == '.txt', all_files)  # 文件夹下的所有txt文件
    all_txt_files = [i for i in txt_files]

    for i in all_txt_files:
        src = src_dir + "\\" + i
        dst = target_dir + "\\" + "flip_" + i
        shutil.copyfile(src, dst)

    print("%d txts saved to %s" % (len(all_txt_files), target_dir))


def create_inverse_trainset(src_dir, target_dir, shuffle=True):
    """
    制造读取方向是反向的数据集, 用来弥补容易过拟合的问题
    shuffle: true -> 打乱  | false -> 反序
    """
    mkdir_if_not_exist(target_dir)

    all_files = os.listdir(src_dir)
    txt_files = filter(lambda x: x[-4:] == '.txt', all_files)  # 文件夹下的所有txt文件
    all_txt_files = [i for i in txt_files]

    if shuffle:  # shuffle=False时创建反向排序的数据集
        random.shuffle(all_txt_files)

    curr_num = 0
    pbar = tqdm(reversed(all_txt_files), desc="doing shuffle: ")
    for i in pbar:
        curr_num_str = str(curr_num).zfill(5) + "_"
        src = src_dir + "\\" + i
        dst = target_dir + "\\" + curr_num_str + i
        shutil.copyfile(src, dst)

        src_img1 = src_dir + "\\" + i[:-4] + ".jpg"  # .txt去掉
        src_img2 = src_dir + "\\" + i[:-4] + ".png"

        if Path(src_img1).is_file():
            dst_img = target_dir + "\\" + curr_num_str + i[:-4] + ".jpg"
            shutil.copyfile(src_img1, dst_img)
        elif Path(src_img2).is_file():
            dst_img = target_dir + "\\" + curr_num_str + i[:-4] + ".png"
            shutil.copyfile(src_img2, dst_img)
        curr_num += 1

    print("%d txts saved to %s" % (len(all_txt_files), target_dir))


def do_remove_info(src_dir, target_dir, add_suffix: bool, new_meta: str):
    """
    读取src_dir图片, 抹除水印后复制到target_dir
    :param src_dir:
    :param target_dir:
    :param add_suffix: 是否在文件里加入_cleaned后缀
    :param new_meta: 去除水印后填入的新水印
    :return:
    """
    mkdir_if_not_exist(target_dir)
    image_files = get_image_files(src_dir)
    n_imgs = len(image_files)

    # 多线程, 并发
    # Process the images using ThreadPoolExecutor
    with tqdm(total=n_imgs, desc="remove info: ") as pbar:
        with ThreadPoolExecutor() as executor:
            # Submit a task for each image file to be processed by a thread
            tasks = [executor.submit(
                remove_watermark_single, src_dir, target_dir, filename, add_suffix, new_meta)
                for filename in image_files]

            # Update the progress bar as tasks are completed
            for task in tasks:
                task.add_done_callback(lambda _: pbar.update())

            # Wait for all tasks to complete
            for task in tasks:
                task.result()


def remove_watermark_single(src_dir, target_dir, filename, add_suffix, new_meta):
    """
    https://stackoverflow.com/questions/67963988/
    how-do-i-remove-custom-information-in-a-png-image-file-that-ive-previously-adde
    :param src_dir:
    :param filename:
    :param target_dir:
    :param add_suffix: 是否在文件里加入_cleaned后缀
    :param new_meta: new_meta为空时不添加metadata
    :return:
    """
    path = src_dir + "/" + filename
    suffix = Path(path).suffix.lower()

    if suffix == ".jpg":
        targetImage = JpegImageFile(path)
    elif suffix == ".png":
        targetImage = PngImageFile(path)
    elif suffix == ".webp":
        targetImage = WebPImageFile(path)
    else:
        print("%s 不是有效文件: %s" % (suffix, path))
        exit()

    metadata = PngInfo()

    if new_meta:
        meta_text = new_meta
        metadata.add_text('Notes', meta_text)

    # new_meta为空时不添加metadata

    copyTarget = targetImage.copy()
    if add_suffix:
        copyTarget.save(target_dir + "/" + filename + '_cleaned.png', pnginfo=metadata)
    else:
        copyTarget.save(target_dir + "/" + filename, pnginfo=metadata)


def read_img_prompt_from_dir(src_dir) -> List[str]:
    """"D:\APP\\0CSC\stable-diffusion-webui\outputs\\txt2img-images\好prompt"
    """

    all_files = os.listdir(src_dir)
    jpg_files = [i for i in filter(lambda x: x[-4:] == '.jpg', all_files)]  # 文件夹下的所有txt文件
    png_files = [i for i in filter(lambda x: x[-4:] == '.png', all_files)]

    all_prompts = []
    for i in png_files:
        full_path = src_dir + "\\" + i
        targetImage = PngImageFile(full_path)
        currinfo = targetImage.info
        if currinfo and 'parameters' in currinfo:
            img_params = targetImage.info['parameters'].split('\n')
            all_prompts.append(img_params[0])  # 第一行是正prompt

    for i in jpg_files:
        full_path = src_dir + "\\" + i
        targetImage = JpegImageFile(full_path)

        exif = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in targetImage._getexif().items()
            if k in PIL.ExifTags.TAGS
        }
        comment = exif['UserComment'].decode().replace('\x00', '').split('\n')
        actual_prompt = comment[0][len("UNICODE"):]
        all_prompts.append(actual_prompt)

    return all_prompts


def paste_list_to_clipboard(prompt_list):
    clipboard = ""
    for p in prompt_list:
        clipboard += p + "\n"

    pyperclip.copy(clipboard[:-1])  # 复制到剪贴板, 去掉最后一个\n
    spam = pyperclip.paste()
    print("已复制%d行到剪贴板" % len(prompt_list))


# ==========实际调用==================


def purge_info(src_dir, target_dir, move_dir):
    """读取src_dir图片, 抹除水印后复制到target_dir, 并把原先src_dir的图片移动到move_dir"""
    do_remove_info(src_dir, target_dir, add_suffix=True, new_meta="upscaled by Topaz Gigapixel AI")
    move_images(src_dir, move_dir)



def do_get_prompts(src_dir):
    """复制src_dir里所有图片正面tag, 输出到剪贴板
    DIR1 = "D:\APP\\0CSC\stable-diffusion-webui\outputs\\txt2img-images\好prompt"
    """
    all_prompts = []

    for i in [src_dir]:
        all_prompts += read_img_prompt_from_dir(i)

    paste_list_to_clipboard(all_prompts)
    return all_prompts


def do_flip(src_dir, target_dir):
    """在target_dir创建src_dir图片的翻转版, 并复制txt到旁边
    """
    flip_all_imgs(src_dir, target_dir)
    copy_all_txts(src_dir, target_dir)


def do_shuffle(src_dir, target_dir):
    """打乱src_dir数据集顺序, 输出到target_dir
    """
    create_inverse_trainset(src_dir, target_dir, shuffle=True)


if __name__ == '__main__':
    SOURCE_DIR = "D:\Andrew\Pictures\\fold\miniset"
    TARGET_DIR = "D:\Andrew\Pictures\\fold\miniset"
    flip_single_image(SOURCE_DIR, TARGET_DIR, "1.png")

    # 去水印, 实用版 (添加upscaled by Topaz Gigapixel AI)

    purge_info("O:\===分拣===\.已升分辨率", "O:\===分拣===\.ada已抹除水印", "O:\===分拣===\.已升分辨率\done")
    # 移动原图
    move_images("O:\===分拣===\.升分辨率", "O:\===分拣===\.升分辨率\done")


    # 复制文件夹prompt到剪贴板
    # do_get_prompts(SOURCE_DIR, TARGET_DIR)

    # 翻转图片
    # do_flip(SOURCE_DIR, TARGET_DIR)

    # 打乱图片
    # do_shuffle(SOURCE_DIR, TARGET_DIR)
