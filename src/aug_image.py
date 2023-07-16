import base64
import os
from io import BytesIO

import PIL.ExifTags

from tqdm import tqdm
from PIL.PngImagePlugin import PngImageFile, PngInfo
from PIL.JpegImagePlugin import JpegImageFile
from typing import *
from helpers import *




import os
import random
import shutil
from pathlib import Path

from cv2 import cv2


def flip_all_imgs(src_dir, target_dir):
    all_files = os.listdir(src_dir)
    jpg_files = filter(lambda x: x[-4:] == '.jpg', all_files)  # 文件夹下的所有txt文件
    png_files = filter(lambda x: x[-4:] == '.png', all_files)
    all_image_files = [i for i in jpg_files] + [j for j in png_files]

    for i in all_image_files:
        flip_single_image(src_dir, target_dir, i)
    print("%d imgs saved to %s" % (len(all_image_files), target_dir))


def copy_all_txts(src_dir, target_dir):
    all_files = os.listdir(src_dir)
    txt_files = filter(lambda x: x[-4:] == '.txt', all_files)  # 文件夹下的所有txt文件
    all_txt_files = [i for i in txt_files]

    for i in all_txt_files:
        src = src_dir + "\\" + i
        dst = target_dir + "\\" + "flip_" + i
        shutil.copyfile(src, dst)

    print("%d txts saved to %s" % (len(all_txt_files), target_dir))


def create_inverse_trainset(src_dir, target_dir):
    """
    制造读取方向是反向的数据集, 用来弥补容易过拟合的问题
    """
    all_files = os.listdir(src_dir)
    txt_files = filter(lambda x: x[-4:] == '.txt', all_files)  # 文件夹下的所有txt文件
    all_txt_files = [i for i in txt_files]

    random.shuffle(all_txt_files)
    curr_num = 0
    for i in reversed(all_txt_files):
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

        print("D")

    print("%d txts saved to %s" % (len(all_txt_files), target_dir))


def flip_single_image(src_dir, target_dir, filename):
    img = cv2.imread(src_dir + "\\" + filename)
    flippedimage = cv2.flip(img, 1)  # horizontal
    new_name = "flip_" + filename

    cv2.imwrite(target_dir + "\\" + new_name, flippedimage)


def do_flip():
    SOURCE_DIR = "D:\Andrew\Pictures\Grabber\combine12.mai.eagle.768"
    TARGET_DIR = "D:\Andrew\Pictures\Grabber\combine12.mai.eagle.768.flip"
    SAMPLE_IMG = "D:\Andrew\Pictures\Grabber\\test\\1.jpg"

    flip_all_imgs(SOURCE_DIR, TARGET_DIR)
    copy_all_txts(SOURCE_DIR, TARGET_DIR)


def remove_watermarks(file_path, filename, output_path, no_watermark:bool=False):
    """
    https://stackoverflow.com/questions/67963988/
    how-do-i-remove-custom-information-in-a-png-image-file-that-ive-previously-adde
    """

    targetImage = PngImageFile(file_path)

    metadata = PngInfo()

    meta_text = "██╗░░░██╗  ░█████╗░  ██████╗░  ░█████╗░  ██╗\n" \
                "╚██╗░██╔╝  ██╔══██╗  ██╔══██╗  ██╔══██╗  ██║\n" \
                "░╚████╔╝░  ███████║  ██║░░██║  ███████║  ██║\n" \
                "░░╚██╔╝░░  ██╔══██║  ██║░░██║  ██╔══██║  ╚═╝\n" \
                "░░░██║░░░  ██║░░██║  ██████╔╝  ██║░░██║  ██╗\n" \
                "░░░╚═╝░░░  ╚═╝░░╚═╝  ╚═════╝░  ╚═╝░░╚═╝  ╚═╝\n"
    if no_watermark:
        meta_text="upscaled by Topaz Gigapixel AI"

    metadata.add_text('Notes', meta_text)


    copyTarget = targetImage.copy()
    copyTarget.save(output_path+ "/"+filename+'_cleaned.png', pnginfo=metadata)


def read_img_prompt_from_dir(src_dir) -> List[str]:
    """"D:\APP\\0CSC\stable-diffusion-webui\outputs\\txt2img-images\好prompt"
    """

    all_files = os.listdir(src_dir)
    jpg_files = [i for i in filter(lambda x: x[-4:] == '.jpg', all_files)]  # 文件夹下的所有txt文件
    png_files = [ i for i in filter(lambda x: x[-4:] == '.png', all_files)]

    all_prompts = []
    for i in png_files:
        full_path = src_dir + "\\" + i
        targetImage = PngImageFile(full_path)
        img_params = targetImage.info['parameters'].split('\n')
        all_prompts.append(img_params[0]) # 第一行是正prompt

    for i in jpg_files:
        full_path = src_dir + "\\" + i
        targetImage = JpegImageFile(full_path)

        exif = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in targetImage._getexif().items()
            if k in PIL.ExifTags.TAGS
        }
        comment = exif['UserComment'].decode().replace('\x00','').split('\n')
        actual_prompt = comment[0][len("UNICODE"):]
        all_prompts.append(actual_prompt)

    return all_prompts

# ==========实际调用==================



def do_remove():
    addr = "O:\===分拣===\.已升分辨率"
    IMG_OUT_DIR = 'O:\===分拣===\.ada已抹除水印'
    # IMG_OUT_DIR = 'O:\===分拣==='

    global all_tags_list
    all_files = os.listdir(addr)
    png_files = filter(lambda x: x[-4:] == '.png', all_files)  # 文件夹下的所有txt文件
    pbar = tqdm([i for i in png_files])
    for i in pbar:
        pbar.set_description("去除水印: ")
        path = addr + "/" + i
        # remove_watermarks(path, i, IMG_OUT_DIR, no_watermark=True)
        remove_watermarks(path, i, IMG_OUT_DIR)



def do_flip_img():
    SOURCE_DIR = "D:\Andrew\Pictures\Grabber\combine12.mai.eagle.768"
    TARGET_DIR = "D:\Andrew\Pictures\Grabber\mks_shuffle2"
    create_inverse_trainset(SOURCE_DIR, TARGET_DIR)

def do_get_prompts():
    """目录里所有正面tag变为list输出到剪贴板
    """
    all_prompts = []
    DIR1 = "D:\APP\\0CSC\stable-diffusion-webui\outputs\\txt2img-images\好prompt"

    for i in [DIR1]:
        all_prompts += read_img_prompt_from_dir(i)

    paste_list_to_clipboard(all_prompts)
    return all_prompts



if __name__ == '__main__':

    do_remove()
    # do_remove(IMG_IN_DIR)
    # remove_watermarks("bin/remove_watermark_sample.png")




