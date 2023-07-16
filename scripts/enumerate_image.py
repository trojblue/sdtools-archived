"""给出目录src_dir, 复制所有目录里的所有图片文件到dst_dir
"""
from sdtools.fileops import *
from sdtools.globals import *

def do_enumerate_image(src_dir, dst_dir):
    """把分散在不同文件夹里的训练集复制到同一个文件夹里
    """
    text_files = ['.txt']
    target_suffix = ALL_IMGS + text_files

    # 文件夹里只有图片和txt
    bad_files = check_file_suffix(src_dir, target_suffix)
    if bad_files:
        print(bad_files)

    # 复制src_dir内所有子文件到dst_dir
    enumerate_files_to_dir(src_dir, dst_dir, target_suffix, recursive=True, move=False)



if __name__ == '__main__':
    src_dir = 'D:\Andrew\Pictures\Grabber\combine4'
    dst_dir = 'D:\Andrew\Pictures\Grabber\combine4_ALL'


    do_enumerate_image(src_dir, dst_dir)




