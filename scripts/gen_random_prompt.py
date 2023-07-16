import random
from sdtools.config_gen import *
from sdtools.prompt_settings import PromptSettings
from t2 import gen_prompt
from sdtools.globals import *


def gen_prompts():

    # d0c_nice, colab, hires fix, 很nb

    mecha_settings = PromptSettings(
        start_word="",
        vital_tags="1girl, (best quality), by gyndroid," + ", ".join(mecha_tags),
        end_tags="gyndroid, original, highres",
        taboo_tags=longer_taboo_tags + simple_miku_tags
    )
    kbr_settings = PromptSettings(
        start_word="",
        vital_tags="1girl, (best quality), by kobaryo, album cover, chromatic abbrevation, hood",
        end_tags="original, highres, by kobaryo",
        taboo_tags=longer_taboo_tags + simple_miku_tags
    )

    niko_settings = PromptSettings(
        start_word="sks, a clean painting of",
        vital_tags="1girl, (best quality:1.3), yada",
        end_tags="z3zz4, original, highres",
        taboo_tags=longer_taboo_tags
    )

    bench_settings = PromptSettings(
        start_word="",
        vital_tags="1girl, (best quality)",
        end_tags="original, highres",
        taboo_tags=longer_taboo_tags + simple_miku_tags
    )

    sexy_words = "sexy, medium breasts, legs, nice body, thighhighs, " \
                 "(masterpiece:0.1), skindentation".split()
    sexy_words_new = " ".join(i for i in sexy_words)

    sexy_settings = PromptSettings(
        start_word="",
        vital_tags="1girl, (best quality), beautiful detailed eyes" + sexy_words_new,
        end_tags="original, highres",
        taboo_tags=longer_taboo_tags
    )

    mai_aug_settings = PromptSettings(
        start_word="",
        vital_tags="1girl, (best quality), beautiful detailed eyes" + sexy_words_new,
        end_tags="original, highres",
        taboo_tags=longer_taboo_tags
    )

    shitstorm_settings = PromptSettings(
        start_word= shitstorm_pos,
        vital_tags="1girl, (best quality), beautiful detailed eyes, sexy, medium breasts, legs, nice body, thighhighs, (masterpiece:0.1), skindentation,",
        # end_tags=shitstorm_neg_actual,
        taboo_tags="simple background, username"+simple_miku_tags

    )

    gs = niko_settings
    gen_prompt(tag_count=35, line_count=100, gs=gs)


def get_simple_random_prompt():
    import random

    start_str = "mecha_tags clean painting of ((1girl)), best quality, "

    description_tags = "solo, red hair, palace, carpet, royal, town, bangs, medium hair, long sleeves, blue rose, striped, rose, long hair, elf, alternative costume, crown".split(", ")

    christmas_tags = "jingle bell, official art, shawl, shorts, christmas ornaments, scenery, snow, gift, full body, confetti, postage stamp, stuffed toy, tassle, white flower, (close-up:0.5), fur collar, scenery, christmas tree".split(', ')

    end_str = "original"
    [random.shuffle(i) for i in (description_tags, christmas_tags)]

    christmas_prompt = start_str +  ', '.join(description_tags) + \
        ', '.join(random.sample(christmas_tags, k=10)) + end_str

    print(christmas_prompt)

def get_complex_christmas_prompt():

    description_tags = "solo, white hair, palace, carpet, royal, town, bangs, long hair, long sleeves, blue rose, striped, rose, alternative costume,  crown".split(", ")
    christmas_tags = "jingle bell, official art, shawl, shorts, christmas ornaments, scenery, snow, gift, full body, confetti, postage stamp, robot girl, mechanical plate armor, gyndroid, mecha girl, stuffed toy, tassle, white flower, (close-up:0.5), fur collar, scenery, christmas tree".split(', ')
    [random.shuffle(i) for i in (description_tags, christmas_tags)]

    christmas_settings = PromptSettings(
        start_word="mecha_tags clean painting of" ,
        vital_tags="1girl, (best quality), beautiful detailed eyes, " +  ', '.join(description_tags) + ', '.join(random.sample(christmas_tags, k=15)),
        end_tags="original, highres",
        taboo_tags=longer_taboo_tags
    )

    gs = christmas_settings
    gen_prompt(tag_count=40, line_count=100, gs=gs)


if __name__ == '__main__':
    gen_prompts()
    # print(shitstorm_neg_actual)




