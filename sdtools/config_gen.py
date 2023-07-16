import random
from typing import Any

from sdtools.prompt_settings import PromptSettings
from sdtools.globals import always_taboo_words




longer_taboo_tags = "blush, antlers, umbrella, white umbrella, bruise,horns, jack-o'-lantern, heterochromia, ball gag, gag, condom, tape gag, wings, angel wings, deveil wings"

simple_miku_tags = "hatsune_miku, headphones, vocaloid, yoneyama_mai, maimuro,sketch"

intricate_starter = "mecha_tags clean painting of 1girl, (best quality), (masterpiece:0.5), (close-up:0.3), by sks, (detailed:0.3), dynamic angle, depth of field, (intricate:0.6)"

main_settings = PromptSettings(
    start_word="mecha_tags clean painting of ",
    vital_tags="(best quality:1.3), by sks,1girl, close-up, face focus",
    end_tags="neco, original, highres",
    taboo_tags= longer_taboo_tags
)

intricate_settings = PromptSettings(
    start_word=intricate_starter,
    vital_tags="",
    end_tags="z3zz4, original, highres",
    taboo_tags=longer_taboo_tags
)

punk_settings = PromptSettings(
    start_word="",
    vital_tags="1girl, (best quality), beautiful detailed eyes, hyper-kawaii, acid punk underground style, face focus",
    end_tags="z3zz4, original, highres",
    taboo_tags=longer_taboo_tags
)


# 群友的
mecha_tags = "mecha girl, mechanical plate armor, mechanical head, cracked, broken metalic textured body, robot girl".split(', ')
random.shuffle(mecha_tags)

mecha_settings = PromptSettings(
    start_word="",
    vital_tags="1girl, (best quality), by gyndroid," + ", ".join(mecha_tags),
    end_tags="gyndroid, original, highres",
    taboo_tags=longer_taboo_tags + simple_miku_tags
)
