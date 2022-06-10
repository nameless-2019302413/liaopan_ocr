from itertools import zip_longest
import pkg_resources
from symspellpy.symspellpy import SymSpell

def replace(x, old, new=None, strip=False) -> str:
    '''批量替换字符串内容

    :param x: 原始字符串
    :param old: 要替换的内容，可为 `str` , `list`
    :param new: 新内容，可为 `str` , `list` , `None`
    :param strip: 是否删除前后空格
'''
    if not new:
        new = ''
    if isinstance(old, str):
        x = x.replace(old, new)

    if isinstance(old, list):
        for _old, _new in zip_longest(old, new, fillvalue=''):
            if _new == None:
                _new = ''
            x = x.replace(_old, _new)
    if strip:
        x = x.strip()
    return x


with open(r'1.txt',"r") as f:
    str_1 = f.read()

replace(str_1,old='0',new='o')
replace(str_1,old='2',new='e')

str_2=str_1.lower()


sym_spell = SymSpell(max_dictionary_edit_distance=0, prefix_length=7)
dictionary_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_dictionary_en.txt")

sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

# a sentence without any spaces
input_term = "thequickbrownfoxjumpsoverthelazydog"
result = sym_spell.word_segmentation(str_2)



