from typing import Any

from sdtools.globals import always_taboo_words


def split_ifexist(list_string: str, else_word: Any):
    """如果list_string非空, 返回list_string.split(', )
    否则返回else_word
    """
    return list_string.split(', ') if list_string else else_word


class PromptSettings():
    def __init__(self, start_word="",
                 vital_tags: str = "",
                 end_tags: str = "",
                 mashup_tags: str = "",
                 taboo_tags: str = "",
                 accent_tags: str = None,
                 accent_count: int = 0
                 ):
        """start - vital - [  mashup+random ] - end
        输入为string, 保存在class内时为list
        """
        self.start_word = split_ifexist(start_word, "")
        self.vital_tags = split_ifexist(vital_tags, [])
        self.end_tags = split_ifexist(end_tags, [])
        self.mashup_tags = split_ifexist(mashup_tags, [])
        self.taboo_tags = split_ifexist(taboo_tags, []) + always_taboo_words
        self.accent_tags = split_ifexist(accent_tags, [])
        self.accent_count = accent_count