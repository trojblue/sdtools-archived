from sdtools.aug_image import *

def do_flip_imgs(path):
    """
    在原地创建翻转的数据集, 并打乱
    """

    # 打乱图片
    inversed = os.path.join(path, "inversed")
    create_inverse_trainset(path, inversed, shuffle=True, filename=False)


if __name__ == '__main__':

    path = input("输入path:")
    do_flip_imgs(path)