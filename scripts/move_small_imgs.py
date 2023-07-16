
from sdtools.fileops import *




if __name__ == '__main__':

    # 移动src_dir里短边小于512的图片到 src_dir/sub512
    src_dir = 'D:\Andrew\Pictures\=训练扩充COMBINED'
    limit = 512

    move_smaller_imgs(src_dir, src_dir+"\SUB512", limit)




