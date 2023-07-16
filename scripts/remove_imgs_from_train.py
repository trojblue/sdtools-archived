
import argparse



def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--src_dir",
        type=str,
        default="sd-model-finetuned",
        help="The source directory of training image/texts."
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="sd-model-finetuned",
        help="The out directory for removed image/texts."
    )





def main():
    args = parse_args()




if __name__ == '__main__':
    pass