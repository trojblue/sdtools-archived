"""文字型的变量
"""
import random

default_train_set = "D:\Andrew\Pictures\Grabber\c123Eagle.OG"

trash_tags_raw = "bad_id, bad_twitter_id, bad_link, commentary, commentary_request, translation_request, " \
                 "mixed-language_commentary, tagme, english_commentary, commentary, symbol-only_commentary, " \
                 "mixed-language_commentary, dated_commentary, check_commentary, chinese_commentary, " \
                 "romaji_commentary, partial_commentary, weibo_username, white_watermark, sample_watermark, holding chopsticks, twitter username, korean commentary, korean commentary"

trash_tags = trash_tags_raw.split(", ")

always_taboo_words = (
            "1_girl, 6+girls, no_humans, 1boy, 2boys, male focus, guro, closed eyes, halloween" + trash_tags_raw).split(
    ', ')

meta_text = "██╗░░░██╗  ░█████╗░  ██████╗░  ░█████╗░  ██╗\n" \
            "╚██╗░██╔╝  ██╔══██╗  ██╔══██╗  ██╔══██╗  ██║\n" \
            "░╚████╔╝░  ███████║  ██║░░██║  ███████║  ██║\n" \
            "░░╚██╔╝░░  ██╔══██║  ██║░░██║  ██╔══██║  ╚═╝\n" \
            "░░░██║░░░  ██║░░██║  ██████╔╝  ██║░░██║  ██╗\n" \
            "░░░╚═╝░░░  ╚═╝░░╚═╝  ╚═════╝░  ╚═╝░░╚═╝  ╚═╝\n"

neg_realistic = "nsfw, text, error, signature, watermark, username, multiple people, animals, lowres, cropped, worth quality ,low quality, normal quality, jpeg artifacts, blurry, bad hands, bad arms, bad feet, bad anatomy, missing fingers, extra digits, fewer digits, long neck, missing legs, huge person, optical_illusion, masterpiece"

neg_shitstorm = "lowres, bad anatomy, bad hands, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, bad anatomy, bad hands, low quality, low quality, watermark, username, blurry, bad anatomy, bad hands, low quality, low quality, watermark, username, blurry, bad anatomy, bad hands, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low qualitymissing fngers, scan, gay, cropped, simple background, cropped, missing fngers, simple background, low quality, scan, lowres lowres murder,Coprophilia, simple background, low quality, unfinished picture,  low quality, gay,  low quality, unfinished picture,  low quality, unfinished picture, cropped, cropped, lowres, unfinished picture, cropped, fewer digits, extra digt, bonelow qualitylow qualitylow qualitylow qualitylow qualitylow quality, scan, missing fngers, unfinished picture, low quality, simple background, low quality, lowres, bonelow qualitylow qualitylow qualitylow quality"


neg_longer_hands = "nsfw, text, error, signature, watermark, username,multiple people, animals, lowres, cropped, worth quality, low quality, normal quality, jpeg artifacts, blurry, bad hands, bad arms, bad feet, bad anatomy, missing fingers, extra digits, fewer digits, fused digit, missing digit, bad digit, liquid digit, (mutated hands and fingers), malformed limbs, bad hands, fused hand, missing hand, disappearing arms, gross proportions, long neck, missing legs, disappearing calf, disappearing legs, fused ears, bad ears, huge person, optical_illusion, masterpiece"

neg_longer_hands_masterpiece = "nsfw, text, error, signature, watermark, username,multiple people, animals, lowres, cropped, worth quality, low quality, normal quality, jpeg artifacts, blurry, bad hands, bad arms, bad feet, bad anatomy, missing fingers, extra digits, fewer digits, fused digit, missing digit, bad digit, liquid digit, (mutated hands and fingers), malformed limbs, bad hands, fused hand, missing hand, disappearing arms, gross proportions, long neck, missing legs, disappearing calf, disappearing legs, fused ears, bad ears, huge person, optical_illusion"


smurf_neg = "text, ui, error, cropped, watermark, username, blurry, JPEG artifacts, signature, worst quality ,low quality, normal quality,(mutated hands and fingers), (long body), (mutation, poorly drawn) , black-white, bad anatomy, liquid body, disfigured, malformed, mutated, anatomical nonsense, text font ui, error, malformed hands, long neck, blurred, lowers, lowres, bad anatomy, bad proportions, bad shadow, uncoordinated body, unnatural body, multiple breasts, fused breasts, bad breasts, poorly drawn breasts, huge haunch, huge thighs, huge calf, huge person, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, fused ears, bad ears, poorly drawn ears, extra ears, liquid ears, missing ears, missing fingers, missing limb, fused fingers, one hand with more than 5 fingers, one hand with less than 5 fingers, one hand with more than 5 digit, one hand with less than 5 digit, extra digit, fewer digits, fused digit, missing digit, bad digit, liquid digit, malformed feet, extra feet, bad feet, poorly drawn feet, fused feet, missing feet, extra shoes, bad shoes, fused shoes, more than two shoes, poorly drawn shoes, bad gloves, poorly drawn gloves, fused gloves, big muscles, ugly, malformed limbs, gross proportions. short arm, missing arms, missing thighs, missing calf, missing legs, mutation, optical illusion"


shitstorm_pos = " masterpiece, best quality, (masterpiece), (best quality), (highres), ( extremely detailed cg), (ultra-detailed), (llustration)"
shitstorm_neg_starter = "nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, bad anatomy, bad hands, low quality, low quality, watermark, username, blurry, bad anatomy, bad hands, low quality, low quality, watermark, username, blurry, bad anatomy, bad hands, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality, low quality"
shitstorm_neg_accent = "low quality, lowres, unfinished picture, simple background, gay, missing fngers, extra digt, fewer digits, cropped,  low quality, low quality, lowres lowres murder,Coprophilia, scan, bone" + "low quality"*5
shitstorm_new = (shitstorm_neg_accent*5).split(', ')
random.shuffle(shitstorm_new)
shitstorm_neg_actual = shitstorm_neg_starter + ", ".join(shitstorm_new)


# ======================RUNTIME
NON_JPG_PNG_IMGS = ['.bmp', '.gif', '.webp', '.tiff']
NON_PNG_IMGS =  ['.jpg', 'jpeg', '.bmp', '.gif', '.webp', '.tiff']


# https://docs.python.org/3/library/imghdr.html
__all_imgs_raw = "jpg jpeg png bmp dds exif jp2 jpx pcx pnm ras gif tga tif tiff xbm xpm webp"
ALL_IMGS =  ["."+i.strip() for i in __all_imgs_raw.split(" ")]