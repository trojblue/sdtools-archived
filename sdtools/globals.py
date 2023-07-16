"""文字型的变量
"""
default_train_set = "D:\Andrew\Pictures\Grabber\c123Eagle.OG"

trash_tags_raw = "bad_id, bad_twitter_id, bad_link, commentary, commentary_request, translation_request, " \
                 "mixed-language_commentary, english_commentary, commentary, symbol-only_commentary, " \
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
