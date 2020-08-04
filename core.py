from pykakasi import kakasi
import json
from copy import deepcopy
from utils import *


def get_dic_and_conv(dict_path):
    print('Loading dict from', dict_path)
    print()
    file = open(dict_path, 'r', encoding='utf-8')
    d = json.loads(file.read())
    file.close()

    k = kakasi()
    k.setMode('H', 'a')
    k.setMode('K', 'a')
    k.setMode('J', 'a')
    conv = k.getConverter()
    return d, conv


def get_word_romaji(dic, word):
    if word in dic.keys():
        return deepcopy(dic[word])
    else:
        return []


def spaces(num):
    result = ''
    for i in range(num):
        result += ' '
    return result


def get_sentence_romaji(dic, sentence, conv):
    sentence_split = []
    romaji_split = []
    start = 0
    while start < len(sentence):
        for end in range(len(sentence), start, -1):
            word_temp = sentence[start:end]
            romaji = get_word_romaji(dic, word_temp)
            if len(romaji) > 0:
                if word_temp == 'へ' or word_temp == 'ヘ':
                    romaji = ['e']
                sentence_split.append(word_temp)
                romaji_split.append(romaji)
                start = end - 1
                break
            elif len(romaji) == 0 and len(word_temp) == 1:
                sentence_split.append(word_temp)
                romaji = [conv.do(word_temp)]
                romaji_split.append(romaji)
                start = end - 1
                break
        start += 1

    for i in range(len(sentence_split)):
        if sentence_split[i][-1] == 'っ' and i != len(sentence_split) - 1:
            for j in range(len(romaji_split[i + 1])):
                temp = romaji_split[i + 1][j]
                if len(temp) >= 2 and temp[0] == temp[1]:
                    continue
                romaji_split[i + 1][j] = temp[0] + temp
            for j in range(len(romaji_split[i])):
                temp = romaji_split[i][j]
                if len(temp) >= 3 and temp[-3:] == 'tsu':
                    romaji_split[i][j] = temp[:-3]

    return sentence_split, romaji_split


def get_size(sentence):
    len_txt = len(sentence)
    len_txt_utf8 = len(sentence.encode('utf-8'))
    size = int((len_txt_utf8 - len_txt) / 2 + len_txt)
    return size


def format_print(words, romaji_split):
    # find max number
    romajis = deepcopy(romaji_split)
    max_num = 0
    for romaji in romajis:
        if len(romaji) > max_num:
            max_num = len(romaji)
            # print(romaji)

    for i in range(len(words)):
        romajis_one_word = romajis[i]
        # find the max len
        max_len = get_size(words[i])
        for romaji in romajis_one_word:
            if get_size(romaji) > max_len:
                max_len = get_size(romaji)
        # fill spaces
        while get_size(words[i]) < max_len:
            words[i] += ' '
        for j in range(len(romajis[i])):
            while get_size(romajis[i][j]) < max_len:
                romajis[i][j] += ' '
        while len(romajis[i]) < max_num:
            romajis[i].append(spaces(max_len))

    result = ''
    for word in words:
        result = result + word + ' '
    result += '\n'

    for i in range(max_num):
        for romaji in romajis:
            result += romaji[i] + ' '
        result += '\n'
    return result


def translate_all(content):
    user_input = content.split('\n')
    result = ''
    for sentence in user_input:
        s, r = get_sentence_romaji(d, sentence, c)
        result += format_print(s, r)
    while '\n\n' in result:
        result = result.replace('\n\n', '\n')
    return result


def front_match(s, front):
    if len(front) > len(s):
        return False
    for i in range(len(front)):
        if front[i] != s[i]:
            return False
    return True


def replace_ha_with_wa(sentence):
    result = deepcopy(sentence)
    while '　' in result:
        result = result.replace('　', '')
    while ' ha ' in result:
        result = result.replace(' ha ', ' wa ')
    if len(result) >= 3 and result[0] == 'h' and result[1] == 'a' and result[2] == ' ':
        result[0] = 'w'
    if len(result) >= 3 and result[-3] == ' ' and result[-2] == 'h' and result[-1] == 'a':
        result[-2] = 'w'
    return result



def translate_default(content, split=False):
    user_input = content.split('\n')
    result = ''
    for sentence in user_input:
        sentence_result = ''
        romaji = c.do(sentence)
        words, romajis = get_sentence_romaji(d, sentence, c)

        for i in range(len(romajis)):
            no_match = True
            for j in range(len(romajis[i])):
                if front_match(romaji, romajis[i][j]):
                    sentence_result += romajis[i][j] + ' '
                    romaji = romaji[len(romajis[i][j]):]
                    no_match = False
                    break
            if no_match:
                sentence_result += romaji
                break
        while ' 　' in sentence_result:
            sentence_result = sentence_result.replace(' 　', ' ')
        while '  ' in sentence_result:
            sentence_result = sentence_result.replace('  ', ' ')
        result += sentence + '\n'
        result += replace_ha_with_wa(sentence_result) + '\n'
    while '\n\n' in result:
        result = result.replace('\n\n', '\n')
    return result


d, c = get_dic_and_conv('d.txt')
if __name__ == '__main__':
    print(get_sentence_romaji(d, 'は', c))
    # print(translate_default('気付いたのは突然だった'))
    # print(c.do('今日も空を眺めるのでしょう'))