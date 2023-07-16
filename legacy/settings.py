"""处理json, 创建预置tag
"""
from typing import *
# default_train_set = "D:\Andrew\Pictures\AI\\20221111.训练.混合.final"
# default_train_set = "D:\Andrew\Pictures\Grabber\combine12.mai.eagle.OG"
# from get_prompt_from_training import get_OG_line_from_train

default_train_set = "D:\Andrew\Pictures\Grabber\c123Eagle.OG"
test_train_set = "D:\Andrew\Pictures\Grabber\\test1"
danbooru_csv = "bin/danbooru-tags.csv"


#
trash_tags_raw = "bad_id, bad_twitter_id, bad_link, commentary, commentary_request, translation_request, " \
                 "mixed-language_commentary, english_commentary, commentary, symbol-only_commentary, " \
                 "mixed-language_commentary, dated_commentary, check_commentary, chinese_commentary, " \
                 "romaji_commentary, partial_commentary, weibo_username, white_watermark, sample_watermark, holding chopsticks, twitter username, korean commentary, korean commentary"

trash_tags = trash_tags_raw.split(", ")

always_taboo_words = ("1_girl, 6+girls, no_humans, 1boy, 2boys, male focus, guro, closed eyes, halloween" + trash_tags_raw).split(', ')



MODEL_NAME = "default_name"
resolution_random = (960, 704)
resolution_random_v = (704, 960)
resolution_illust = (1024, 768)
resolution_illust_verti = (768, 1024)




class GenSettings():
    def __init__(self, start_word=None,
                 vital_tags: str = None, end_tags: str = None, mashup_tags=None, taboo_tags: str = None, accent_tags:str = None,
                 accent_count:int = None, tag_count:int=None
                 ):
        """start - vital - [  mashup+random ] - end
        输入为string, 保存在class内时为list
        """

        self.start_word = start_word if start_word else ""
        self.vital_tags = vital_tags.split(", ") if vital_tags else ["1girl", "best quality"]
        self.end_tags = end_tags.split(", ") if end_tags else []
        self.mashup_tags = mashup_tags if mashup_tags else []
        self.taboo_tags = taboo_tags.split(", ") + always_taboo_words if taboo_tags else always_taboo_words
        self.accent_tags = accent_tags
        self.accent_count = accent_count if accent_count else 0
        self.tag_count = tag_count if tag_count else 35


normal_vitals = "1girl, best quality, masterpiece, (close-up:1), by sks, hyper detailed, dynamic angle, depth of field, (intricate), beautiful detailed eyes, close-up, face focus"
d0c_nice_vitals_acid = "1girl, (best quality), beautiful detailed eyes, hyper-kawaii, acid punk underground style, face focus, full body"



smurf_settings = GenSettings(
    vital_tags=d0c_nice_vitals_acid,
    taboo_tags="yoneyama mai, maimuro, blush, antlers, umbrella, white umbrella, bruise,horns, jack-o'-lantern, heterochromia, ball gag, gag, tape gag, wings, angel wings, deveil wings",
    end_tags="z3zz4, original, highres",
    accent_tags="center opening, revealing clothes, single thighhigh, earrings, eyelashes, navel, hair ornament, hyperkawaii, harajuku-kei, pantyhose, thigh strap, leg garter, hydrangea, pleated skirt, necklace, socks, neck ribbon, bracelet, white flower, sailor collar, clothing cutout, nice body",
    accent_count= 1
)

benchmark_settings = GenSettings(
    vital_tags="1girl, (best quality), hatsune miku, vocaloid, pose",
    taboo_tags="yoneyama mai, maimuro, blush, antlers, umbrella, white umbrella, bruise,horns, jack-o'-lantern, heterochromia, ball gag, gag, tape gag, wings, angel wings, deveil wings",
    end_tags="original, highres",
    accent_tags="center opening, revealing clothes, single thighhigh, earrings, eyelashes, navel, hair ornament, hyperkawaii, harajuku-kei, pantyhose, thigh strap, leg garter, hydrangea, pleated skirt, necklace, socks, neck ribbon, bracelet, white flower, sailor collar, clothing cutout, nice body",
    accent_count= 2
)

# animesfw + wild_card Hypernet
anime_sfw_settings = GenSettings(
    vital_tags="a clean painting of (best quality:1.5),finely detailed, illustration, ultra-detailed, amazing fine details and brush strokes, 1girl",
    taboo_tags="yoneyama mai, maimuro, blush, antlers, umbrella, white umbrella, bruise,horns, jack-o'-lantern, heterochromia, ball gag, gag, tape gag, wings, angel wings, deveil wings",
    end_tags="(art by wild_card), original, highres",
    accent_tags="center opening, revealing clothes, single thighhigh, earrings, eyelashes, navel, hair ornament, hyperkawaii, harajuku-kei, pantyhose, thigh strap, leg garter, hydrangea, pleated skirt, necklace, socks, neck ribbon, bracelet, white flower, sailor collar, clothing cutout, nice body",
    accent_count= 2,
    tag_count = 50
)


# nail polish出手容易崩去掉了

main_settings = GenSettings(
    start_word="a clean painting of ",
    vital_tags="(best quality:1.3), by sks,1girl, close-up, face focus",
    end_tags="neco, original, highres",
    taboo_tags="twintails, hatsune_miku, headphones, vocaloid, yoneyama_mai, maimuro,"
               "sketch,low_twintails"
)

sex_settings = GenSettings(
    start_word="a clean painting of",
    vital_tags="(best quality:1), by sks, 1girl, nsfw, sexy,  tentacles under clothes, single thighhigh",
    end_tags="original, highres",
    taboo_tags="yoneyama_mai, maimuro,"
               "sketch,low_twintails"
)

gs = anime_sfw_settings  # generate settings


# vital_tags = "(best quality:1), by sks,2girls, nsfw, sexy,  bdsm, bondage,thighhighs, dildo, medium breasts, yuri, pegging, maid apron, cock in thighhigh, sex toys, spread legs, ahegao",

# 大号


# {json组名: 权重}
json_group_weights = {"sex_tags": 2,
                      "remotely_miku_tags": 0.3}



# 临时变量

# 科技风, 绿白废土, 植物; 效果不错
p_green_space = "(best quality:1.3), by sks,1girl, closed mouth, medium breasts, wings, mouth mask, solo, sleeveless, white shirt, looking at viewer, white flower, grey hoodie, blurry, shorts, earrings, grey jacket, full body, fur trim, bruise, , light particles, maimuro, 1girl, open mouth, white hair, washing machine, jacket, thorns, bodysuit, mask, blurry foreground, long hair, bird, grey hair, yoisaki kanade, aqua eyes, arm up, artist name, two-tone ribbon, original, bag, green background, neco, original, highres"

p_birdy = "(best quality:1.3), by sks,1girl, straw hat, rabbit tail, shorts, red bow, bat wings, shirt,  apocalypse, goggles on head, nail polish, bangs, bird, aurora, medium breasts, wings, black skirt, blue eyes, very long hair, white hair,  animal ears, flame, smile, solo, light particles, arm up, ribbon,blurry, instrument, blurry foreground, covered mouth, thorns,  bird cage, oversized_object,   skirt, night sky, barefoot, loose necktie, summer uniform, white flower, black ribbon,hair ribbon, neco, original, highres"


# 以下为prompt变量

# 橙色背景, 白夹克, 机械, miku
p_orange_white_miku = "a clean painting of 1girl, aqua_eyes, aqua_hair, black_gloves, gloves, hatsune_miku, headphones, headset, holding, ((holding_staff)), jacket, close_up, hand_focus, (oversized_object, machine), orange decorations, racing, falling, pilot goggles, long_hair, depth of field, looking_at_viewer, simple_background, solo, staff, thighhighs, twintails, very_long_hair, white_background, white_jacket"


# 白长发, 奶茶, 巨大, 冲击性, 真实光影
p_white_drink_realistic = "a clean painting of (best_quality:1.3), by_sks, 1girl, album_cover, see-through, standing, foreshortening,(neco:1.5), aestheticism, realistic lighting, photorealistic, 4k octane render, from oblique side,hands_up, gestural, dynamic angle, year_of_the_rat, open_mouth, see-through_sleeves, closed_mouth, upper_body, ring, cloud, solo, oni, oversized_object, holding_drink, darkness, rimlight, blurry_foreground, drink, uplight, argyle , blue_eyes, white_hair, long_hair, bare_shoulders, white_flower, shirt, thighhighs, kimono, barefoot, sidelocks, gift_bag, jacket, original, highres"



# 黑皮恶魔
p_black_demon_girl = "(best quality:1.3), by sks,1girl, arm_tattoo, bangs, bracelet, braid, breasts, chest_tattoo, choker, dark-skinned_female, dark_skin, full_body, hair_over_one_eye, horns, jewelry, leg_tattoo, black_hair, long_hair, looking_at_viewer, medium_breasts, multicolored_hair, oni_horns, pendant, red_eyes, sandals, shoulder_tattoo, simple_background, single_horn, solo, tattoo, twin_braids, two-tone_hair, weapon, neco, original, highres"

p_qipao = "1girl, (best quality:1.3), by sks, bare_legs, bare_shoulders, naked, nsfw, revealing clothes, sex toys, braid, braided_bun, branch, breasts, china_dress, chinese_knot, double_bun, ear_piercing, earrings, flower_knot, grey_background, grey_hair, hair_bun, jewelry, looking_at_viewer, medium_breasts, off_shoulder, open_clothes, open_jacket, parted_lips, piercing, pink_eyes, shoes, sleeveless, sleeveless_dress, sneakers, solo, tassel_earrings, thigh_strap, white_dress, white_footwear, neco, original"

p_tenshi = "(best quality:1.3), by sks,1girl, highres, dark background, black bow, tongue, long hair, feathered wings, blurry, aqua hair, bag, double v, upper body, orange slice, head tilt, maid apron, tail, scenery, very long hair, rifle, embers, dress, white feathers, detached sleeves, sleeveless, jewelry, lighthouse, jacket, nail polish, shorts, black footwear, wavy hair, electric fan, simple background, blonde hair, off shoulder, wings, pants, gradient sky, looking at viewer, black scrunchie, neco, original, highres"

p_red_modern = "1girl, (best quality), beautiful detailed eyes, hyper-kawaii, acid punk underground style, (close-up:0.2), album cover, pose, face focus, downtown Toronto, foliage, red footwear, standing, holding, looking at viewer, hood down, grey eyes, two-tone hair, shopfront, Tim Hortons, holding coffee, (graffiti:0.2), white background, bandages, lion ears, bangs, from side, tattoo, blurry foreground, utility pole, white background, z3zz4, absurdres, black gloves, hood, full body, long hair, original, highres"

p_purple_jirai = "a clean illustration of (best_quality:1.3), masterpiece, by sks, 1girl, eye-focus, hyperkawaii, foreshortening, purple pink hair,  :0, (((low_twintails))), long_hair, bangs, (demon_wings), (grey eyes), nails, long puffy sleeves, ((pointy ears)), (short ears), (((((black jacket))))), ribbons, low twintails, [[[sailor collar]]], ahoge, hyper-kawaii, yuzuki_yukari, realistic_lighting, looking_up, (yuzuki_yukari:1) , (bare legs), black boots, ribbons on sleeves, jirai-kei, harajuku-kei, ribbon on sleeves, [[[[art by wild_card]]]], ultra-detailed, amazing fine details and brush strokes"

p_cafe = "(masterpiece, illustration, an extremely delicate and beautiful), long bob cut, apron, uniform, looking at viewer, 1girl, solo, upper body, coffee shop, light ray, (light particles:0.9), [(Paul Hedley):intricate:0.5], warm tone"

p_cake = "1girl, (best quality), hatsune miku, vocaloid, pose, large breasts, sitting, drinking straw, original, orange rose, holding, focused, ahoge, bandaid on cheek, carrot, blue bow, hatsune miku \(append\), slave, cropped jacket, nail polish, shoulder strap, demon wings, solo, dress, tube, cake slice, aqua hair, stick, original, highres"
# ==============   负面   ====================

# 没有realistic, 3d; 去除masterpiece; 保留nsfw
neg_realistic = "nsfw, text, error, signature, watermark, username, multiple people, animals, lowres, cropped, worth quality ,low quality, normal quality, jpeg artifacts, blurry, bad hands, bad arms, bad feet, bad anatomy, missing fingers, extra digits, fewer digits, long neck, missing legs, huge person, optical_illusion, masterpiece"

neg_city = "nsfw, error, signature, watermark, username, multiple people, animals, lowres, cropped, worth quality ,low quality, normal quality, jpeg artifacts, blurry, bad hands, bad arms, bad feet, bad anatomy, missing fingers, extra digits, fewer digits, long neck, missing legs, huge person, optical_illusion, masterpiece"

neg_purple = "nsfw, text, error, signature, watermark, username, realistic,3d,(large breast), multiple people, animals, lowres, cropped, worth quality ,low quality, normal quality, jpeg artifacts, blurry, bad hands, bad arms, bad feet, (bad anatomy), missing fingers, extra digits, fewer digits, long neck, missing legs, bad legs, huge person, optical_illusion,  hatsune miku, thighhighs, ((elf ears))"

neg_longer_hands = "nsfw, text, error, signature, watermark, username,multiple people, animals, lowres, cropped, worth quality, low quality, normal quality, jpeg artifacts, blurry, bad hands, bad arms, bad feet, bad anatomy, missing fingers, extra digits, fewer digits, fused digit, missing digit, bad digit, liquid digit, (mutated hands and fingers), malformed limbs, bad hands, fused hand, missing hand, disappearing arms, gross proportions, long neck, missing legs, disappearing calf, disappearing legs, fused ears, bad ears, huge person, optical_illusion, masterpiece"

smurf_neg = "text, ui, error, cropped, watermark, username, blurry, JPEG artifacts, signature, worst quality ,low quality, normal quality,(mutated hands and fingers), (long body), (mutation, poorly drawn) , black-white, bad anatomy, liquid body, disfigured, malformed, mutated, anatomical nonsense, text font ui, error, malformed hands, long neck, blurred, lowers, lowres, bad anatomy, bad proportions, bad shadow, uncoordinated body, unnatural body, multiple breasts, fused breasts, bad breasts, poorly drawn breasts, huge haunch, huge thighs, huge calf, huge person, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, fused ears, bad ears, poorly drawn ears, extra ears, liquid ears, missing ears, missing fingers, missing limb, fused fingers, one hand with more than 5 fingers, one hand with less than 5 fingers, one hand with more than 5 digit, one hand with less than 5 digit, extra digit, fewer digits, fused digit, missing digit, bad digit, liquid digit, malformed feet, extra feet, bad feet, poorly drawn feet, fused feet, missing feet, extra shoes, bad shoes, fused shoes, more than two shoes, poorly drawn shoes, bad gloves, poorly drawn gloves, fused gloves, big muscles, ugly, malformed limbs, gross proportions. short arm, missing arms, missing thighs, missing calf, missing legs, mutation, optical illusion"


# 2d和谐专用
MY_NEG = "nsfw, text, error, signature, watermark, username, realistic,3d,(large breast), multiple people, lowres, cropped, worth quality ,low quality, normal quality, jpeg artifacts, blurry, bad anatomy, bad hands, bad arms, bad feet, bad anatomy, missing fingers, extra digits, fewer digits, long neck, missing legs, huge person, optical_illusion"

OG_NEG = "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name"


# ===================色色

SEX_TAGS = "small breast, thighhigh, garter belt, ultra-detailed, front view, beautiful detailed eyes, eyebrows, 1girl, bangs, black_nails, collared_shirt, earrings, grey_eyes, jacket, jewelry, long_sleeves, looking_at_viewer, piercing, ring, v, w, naked, bare_shoulders, bdsm, belt_collar, black_collar, barcode_tattoo, collarbone, covering_breasts, handcuffs, bandaid_on_leg, solo, watch, white_shirt, , simple background, city, water_drop, fingernails, ✋, rurudo, underwear, single_thighhigh, skirt, thigh_strap, thighhighs, leg, nice body, bangs, earrings, grey_eyes, jewelry, long_sleeves, looking_at_viewer, green_hair, ring, naked, bare_shoulders, bdsm, frills, collar, holding, collarbone, covering_breasts, center_opening, solo, white background, fingernails, rurudo, underwear, single_thighhigh, skirt, thighhighs, leg, see_through, transparent_raincoat , pool, oversized_object, stuffed_toy, object_hug , azur_lane, virtual_youtuber, vtuber, skirt, see_through, green_hair, ring, bare_shoulders, bdsm, thigh_strap, (sex_toys:1.2), close_up, blindfold, ((bondage, bound together, tied_up, exhibitionism, bondage outfit, vibrator)), wet, saliva, penis, bound together, condom, city, nipple_piercing , nude, :>=, cum_on_body, straddling, gagged, black_blindfold, no_shoes, mirror, netorare, masturbation, collar, holding, collarbone, penis, nipple_rings, white background, fingernails, high heels, rurudo, underwear, bikini, single_thighhigh, leg, pool, virtual_youtuber, breast, thighhigh, halter_dress, front view, 2girls, bangs, boob curtain, sex toys, earrings, grey_eyes, looking_at_viewer, green_hair, ring, bare_shoulders, bdsm, sex_toys, fake_dildo, blindfold, body_writing, ((tied_up)), vibrator, vibrator_on_nipple, nipple_piercing ,_((((grab_another's_Wrist)))),_collar,_leash,_ahegao,_pussy_fuck,_spread_legs,_straddling__,_penis,_cum,_trembling,_First-person_view, bikini, boob curtain, collar, holding, collarbone, covering_breasts, center_opening, solo, white background, fingernails, rurudo, underwear, single_thighhigh, skirt, leg, see_through, naked, bare_shoulders, bdsm, thigh_strap, sex_toys, blindfold, body_writing, ((tied_up)), vibrator, vibrator_on_nipple, nipple_piercing , collar, holding, collarbone, covering_breasts, center_opening, solo, white background, fingernails, rurudo, underwear, single_thighhigh, skirt, leg, see_through, straddling, gagged, black_blindfold, no_shoes, masturbation, collar, transparent_raincoat , pool, azur_lane, backless_dress, frilled_shirt, miniskirt, leg_cutout, garter_straps, oversized_shirt, wet_shirt, leg_ribbon, garter_straps, oversized_shirt, wet_shirt,leg_ribbon, bow_legwear, arm_garter, hagoromo, backless_sweater, casual_one-piece_swimsuit, maid_bikini, living_clothes, anilingus, nipple_tweak, paizuri, bound_wrists, uncensored, wooden_horse, dildo, egg_vibrator, vibrator, vibrator_in_thighhighs, insertion,anal_insertion,large_insertion,fingering,double_penetration,clothed_sex,cock_in_thighhigh,missionary,cowgirl_position,slave,shibari,bdsm,hogtie,public,bra_lift,panties_around_one_leg,walk-in,tally, transformation,insertion,food_insertion,butt_plug,anal_tail,Babydoll,Sexy_lingerie,Transparent_underwear,cat_lingerie,Panties,highleg_panties, bow_panties,implied_yuri,pegging,tentacle_gagged,tentacles_under_clothes,paizuri_on_lap,legs_up,spread_leg,licking_foot,foot_worship,after_buttjob,Pussy_juice,clothed_masturbation,building_sex,breast_grab,nipple_tweak, chikan, compensated_molestation, condom_left_inside, used_condom, anal_beads, completely_nude, shiny_skin, skindentation, skin_tight, wet, bare_shoulders, collarbone, covered_collarbone, neck, underboob_cutout, midriff, navel_cutout, covered_navel, butt_crack, thick_thigh, leg_between_thighs, thigh_gap, thigh_strap, thighlet, thighs, clothes_between_thighs, nipples, areolae, cleavage, covering_breasts, bouncing_breasts, arms_under_breasts, hand_between_breasts, pussy, female_ejaculation, clitoral_stimulation, gag, tongue, saliva, rape, steaming_body, sweating_profusely, body_writing, pubic_tattoo, heart_tattoo, leash_pull, exhibitionism".split(",")
SEX_TAGS = [i.lstrip() for i in SEX_TAGS]



# =================== 预设


preset_DEBUG = {
    "folder_name": "debug",
    "sampler_list": "Euler, Euler a, DDIM".split(", "),
    "step_list": [5, 10],
    "cfg_list": [7],
    "resolution": (512, 512),
    "prompt_list": [p_orange_white_miku]
}

preset_EVAL_SAMPLER = {
    "folder_name": "EVAL_SAMPLER",
    "sampler_list": "Euler, Euler a, DDIM, DPM++ 2M Karras".split(", "),
    "step_list": [15, 20, 25, 31, 39, 52, 69, 120],
    "cfg_list": [7],
    "resolution": (1024, 768),
    "prompt_list": [p_orange_white_miku]
}

preset_STEP_CFG = {
    "folder_name": "STEP_CFG",
    "sampler_list": ["Euler a"],
    "step_list": [i for i in range(16, 26)],
    "cfg_list": [6, 6.5, 7, 7.5, 8],
    "resolution": (1024, 768),
    "prompt_list": [p_orange_white_miku]
}

preset_EVAL_PROMPTS = {
    "folder_name": "EVAL_PROMPTS",
    "sampler_list": "Euler, Euler a, DDIM, DPM++ 2M Karras".split(", "),
    "step_list": [15, 20, 25, 31, 39, 52, 69, 120],
    "cfg_list": [7],
    "resolution": (1024, 768),
    "prompt_list": [p_white_drink_realistic, p_black_demon_girl, p_qipao]
}

preset_EVAL_MODEL = {
    "folder_name": "EVAL_MODEL",
    "sampler_list": "Euler, Euler a, DDIM, DPM++ 2M Karras".split(", "),
    "step_list": [15, 25, 39, 52],
    "cfg_list": [7],
    "resolution": resolution_random,
    "prompt_list": [p_cafe]
}

# 每个batch之间使用完全随机的词条
preset_EVAL_MODEL_RANDOM = {
    "folder_name": "EVAL_MODEL",
    "sampler_list": "Euler, Euler a, DDIM, DPM++ 2M Karras".split(", "),
    "step_list": [15, 25, 39, 52],
    "cfg_list": [7],
    "resolution": resolution_random,
    "prompt_list": []
}

preset_EVAL_MODEL_RANDOM_longer = {
    "folder_name": "preset_EVAL_MODEL_RANDOM_longer",
    "sampler_list": "Euler, Euler a, DDIM, DPM++ 2M Karras, DPM++ 2S a Karras, Heun".split(", "),
    "step_list": [15, 25, 39, 52],
    "cfg_list": [6.5],
    "resolution": resolution_random,
    "prompt_list": []
}

# # 用和训练集一模一样的词条
# preset_TRAIN_PROMPT = {
#     "folder_name": MODEL_NAME + "_TRAIN_PROMPTS",
#     "sampler_list": ["DDIM", "DPM++ 2M Karras", "Euler a"],
#     "step_list": [35],
#     "cfg_list": [6.5],
#     "resolution": resolution_illust_verti,
#     "prompt_list": get_OG_line_from_train(default_train_set, 200)
# }