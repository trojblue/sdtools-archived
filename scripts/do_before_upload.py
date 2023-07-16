from sdtools.aug_image import do_replace_info
from sdtools.utils import move_images


def gen_upload_meta(src_dir, target_dir, move_dir):
    """读取src_dir图片, 抹除水印后复制到target_dir, 并把原先src_dir的图片移动到move_dir
    """
    do_replace_info(src_dir, target_dir, add_suffix=True, new_meta="upscaled by Topaz Gigapixel AI")
    move_images(src_dir, move_dir)



if __name__ == '__main__':
    SOURCE_DIR = "O:\===分拣===\.已升分辨率"
    TARGET_DIR =  "O:\===分拣===\.ada已抹除水印"
    Backup_dir = "O:\===分拣===\.已升分辨率\done"

    gen_upload_meta(SOURCE_DIR, TARGET_DIR, Backup_dir)