from core import *
import argparse


# parser = argparse.ArgumentParser()
# parser.add_argument('-i', '--input', help='input file path')
# parser.add_argument('output', help='output file path')
# args = parser.parse_args()


def separate_a_romaji(romaji):
    result = ''
    vowels = ['a', 'e', 'i', 'ē', 'o', 'u', 'A', 'E', 'I', 'O', 'U', 'ī', 'ō', 'ū']

    for i in range(len(romaji)):

        if romaji[i] in vowels:
            result += romaji[i] + ' '
        elif romaji[i] == 'n' and i + 1 < len(romaji) \
                and romaji[i + 1] not in vowels and romaji[i + 1] != 'y':
            result += romaji[i] + ' '
        else:
            result += romaji[i]

    result = result.replace('  ', ' ')
    if result[-1] == ' ':
        result = result[:-1]

    return result


def get_fifty(path):
    file = open(path, 'r', encoding='utf-8')
    content = file.read()
    file.close()
    fifty = {}
    lines = content.split('\n')
    for line in lines:
        kana = line.split('\t')[0]
        romaji = line.split('\t')[1]
        fifty[romaji] = kana
    return fifty


def romaji2kana(fifty, sentence):
    sentence = sentence.lower()
    sentence = sentence.replace('ja', 'jiya')
    sentence = sentence.replace('chu', 'chiyu')
    sentence = sentence.replace('jo', 'jiyo')
    sentence = separate_a_romaji(sentence)
    romajis = sentence.split(' ')

    result = ''
    for romaji in romajis:
        if len(romaji) >= 3 and romaji[0] == romaji[1]:
            result += 'っ'
            romaji = romaji[1:]
        if romaji in fifty.keys():
            result += fifty[romaji]
        else:
            result += romaji

    return result


def is_kana(c):
    if u'\u30a0' <= c <= u'\u30ff' or u'\u3040' <= c <= u'\u309f':
        return True
    # if c in fifty.values() or c == 'じ' or c == 'づ' or c == 'ず' or c == 'ゅ' or c == 'ゃ' or c == 'ょ':
    #     return True
    return False


def is_chinese(c):
    if u'\u4e00' <= c <= u'\u9fa5':
        if not is_kana(c):
            return True
    else:
        return False


def kanji_attach_kana(src_sentence, romaji):
    kana = romaji2kana(fifty, romaji)
    result = ''
    i = 0
    j = 0
    while i < len(src_sentence) and j < len(romaji):
        if is_kana(src_sentence[i]) and \
                get_sentence_romaji(d, src_sentence[i], c)[1][0][0] == \
                get_sentence_romaji(d, kana[j], c)[1][0][0]:
            result += src_sentence[i]
            i += 1
            j += 1
        elif is_kana(src_sentence[i]) and \
                (get_sentence_romaji(d, src_sentence[i], c)[1][0][0].replace('wa', 'ha') ==
                 get_sentence_romaji(d, kana[j], c)[1][0][0] or
                 get_sentence_romaji(d, src_sentence[i], c)[1][0][0].replace('ha', 'wa') ==
                 get_sentence_romaji(d, kana[j], c)[1][0][0]):
                result += src_sentence[i]
                i += 1
                j += 1
        elif not is_chinese(src_sentence[i]) and not is_kana(src_sentence[i]):
            result += src_sentence[i]
            i += 1
        elif is_chinese(src_sentence[i]):
            length = 0
            while i + length < len(src_sentence):
                if is_kana(src_sentence[i + length]):
                    word = src_sentence[i: i + length]
                    for k in range(j, len(kana)):
                        if get_sentence_romaji(d, kana[k], c)[1][0][0] == \
                                get_sentence_romaji(d, src_sentence[i + length], c)[1][0][0]\
                                or get_sentence_romaji(d, kana[k], c)[1][0][0].replace('wa', 'ha')\
                                == get_sentence_romaji(d, src_sentence[i + length], c)[1][0][0] \
                                and len(word) <= k - j:
                            word_kana = kana[j: k]

                            _, kana2romaji = get_sentence_romaji(d, word_kana, c)
                            romaji_temp = ''
                            for r in kana2romaji:
                                romaji_temp += r[0]
                            romaji_temp = romaji_temp.replace('chiyu', 'chu')
                            romaji_temp = romaji_temp.replace('chiyo', 'cho')
                            romaji_temp = romaji_temp.replace('kiya', 'kya')
                            romaji_temp = romaji_temp.replace('shiya', 'sha')
                            romaji_temp = romaji_temp.replace('jiya', 'jya')
                            romaji_temp = romaji_temp.replace('jiyo', 'jo')
                            romaji_temp = romaji_temp.replace('chiya', 'cha')
                            romaji_temp = romaji_temp.replace('niya', 'nya')
                            romaji_temp = romaji_temp.replace('riya', 'rya')
                            romajis = get_sentence_romaji(d, word, c)[1][0]
                            # for l in range(len(romajis)):
                            #     romajis[l] = romajis[l][0]
                            if romaji_temp not in romajis and romaji_temp.replace('wa', 'ha') not in romajis:
                                continue
                            i += length
                            j = k
                            length = 1000  # to break while loop
                            result += word + '(' + word_kana + ')'
                            break
                elif i + length == len(src_sentence) - 1:
                    word = src_sentence[i:]
                    word_kana = kana[i:]
                    i = 1000  # to break while loop
                    result += word + '(' + word_kana + ')'
                    break
                length += 1
        else:
            print('wrong at', src_sentence, 'skip', 'index', i, j, src_sentence[i])
            return src_sentence
    return result


def get_sentence_type(s):
    if len(s) == 0:
        return None
    for c in s:
        if is_kana(c) or is_chinese(c):
            return 'japanese'
    return 'romaji'


if __name__ == '__main__':
    fifty = get_fifty('五十音图.txt')
    while 1:
       s = input('>')
       kana = romaji2kana(fifty, s)
       print(kana)
       r = input('>')
       print(kanji_attach_kana(s, r))
    # print(kanji_attach_kana('あなたにすべて 奪われてく', 'anata ni subete ubawareteku'))

    # input_file = open(args.input, 'r', encoding='utf-8')
    # content = input_file.read().split('\n')
    # input_file.close()
    
    # output_file = open(args.output, 'w', encoding='utf-8')
    
    # japanese = ''
    # romaji = ''
    
    # for line in content:
        # line_type = get_sentence_type(line)
        # if line_type == 'japanese':
            # japanese = line
        # elif line_type == 'romaji':
            # romaji = line
        # else:
            # continue
        # if japanese != '' and romaji != '':
            # r = kanji_attach_kana(japanese, romaji)
            # japanese = ''
            # romaji = ''
            # output_file.write(r + '\n')
    # output_file.close()
    