from sdtools.aug_image import do_replace_info

"""训练之前去除metadata信息
"""

def purge_info(src, dst):
    do_replace_info(src, dst, add_suffix=True, new_meta="")


if __name__ == '__main__':

    # 训练前完全去除meta信息(不含subdir)
    SOURCE_DIR = "D:\Andrew\Pictures\=训练扩充COMBINED"

    # 保存到子文件夹_cleaned下
    purge_info(SOURCE_DIR, SOURCE_DIR+"\_cleaned")