from sdtools.aug_image import *

def do_flip_imgs(path):
    """
    在原地创建翻转的数据集, 并打乱
    """

    # 创建翻转

    try:
        flip_all_imgs(path, path)
    except Exception as e:
        print(e)

    try:
        copy_all_txts(path, path)
    except Exception as e:
        print(e)

    # 打乱图片
    # inversed = os.path.join(path, "inversed")
    # create_inverse_trainset(path, inversed, shuffle=True)


if __name__ == '__main__':

    path = input("输入path:")
    do_flip_imgs(path)