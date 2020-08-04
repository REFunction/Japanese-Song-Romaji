from core import *
import argparse

debug = False
if not debug:
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='input file path')
    parser.add_argument('output', help='output file path')
    args = parser.parse_args()


kana_dic = {
    'あ': 'ア',
    'い': 'イ',
    'う': 'ウ',
    'え': 'エ',
    'お': 'オ',
    'か': 'カ',
    'き': 'キ',
    'く': 'ク',
    'け': 'ケ',
    'こ': 'コ',
    'さ': 'サ',
    'し': 'シ',
    'す': 'ス',
    'せ': 'セ',
    'そ': 'ソ',
    'た': 'タ',
    'ち': 'チ',
    'つ': 'ツ',
    'て': 'テ',
    'と': 'ト',
    'な': 'ナ',
    'に': 'ニ',
    'ぬ': 'ウ',
    'ね': 'ネ',
    'の': 'ノ',
    'は': 'ハ',
    'ひ': 'ヒ',
    'ふ': 'フ',
    'へ': 'ヘ',
    'ほ': 'ホ',
    'ら': 'ラ',
    'り': 'リ',
    'る': 'ル',
    'れ': 'レ',
    'ろ': 'ロ',
    'わ': 'ワ',
    'を': 'ヲ',
    'だ': 'ダ',
    'ぢ': 'ヂ',
    'づ': 'ヅ',
    'で': 'デ',
    'ど': 'ド',
    'ぁ': 'ァ',
    'ぃ': 'ィ',
    'ぅ': 'ゥ',
    'ぇ': 'ェ',
    'ぉ': 'ォ',
    'ん': 'ン',
    'っ': 'ッ',
}

invert_kana = {value:key for key,value in kana_dic.items()}


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
    while '-' in sentence:
        index = sentence.find('-')
        if index > 0:
            sentence = sentence.replace('-', sentence[index - 1], 1)

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


def get_sentence_type(s):
    if len(s) == 0:
        return None
    for c in s:
        if is_kana(c) or is_chinese(c):
            return 'japanese'
    return 'romaji'


def get_sentence_kana(dic, sentence, conv):
    result = []
    temp = get_sentence_romaji(dic, sentence, conv)
    words = temp[0]
    romajis = temp[1]
    for i, word in enumerate(words):
        if word == 'わ' or word == 'ワ' or word == 'は' or word == 'ハ':
            result.append([word, ['わ', 'は']])
            continue
        if len(word) == 1 and is_kana(word):
            if word in invert_kana.keys():
                result.append([word, [invert_kana[word]]])
            else:
                result.append([word, [word]])
            continue
        if len(romajis[i]) == 1 and romajis[i][0] == '':
            result.append([word, [word]])
            continue
        for j, romaji in enumerate(romajis[i]):
            romajis[i][j] = romaji2kana(fifty, romaji)
        result.append([word, romajis[i]])
    return result


def remove_front(s, front):
    result = deepcopy(s)
    result = result[len(front):]
    return result


def remove_front_same_part(s1, s2):
    # remove same part(front) in s2, return new s2
    for i in range(min(len(s1), len(s2))):
        if s1[i] != s2[i]:
            return s2[i:]
    return s2[min(len(s1), len(s2)):]


def remove_speical_chars(s):
    special_chars = '。，、＇：∶；?‘’“”〝〞ˆˇ﹕︰﹔﹖﹑•¨….¸;！´？！～—ˉ｜' \
                        '‖＂〃｀@﹫¡¿﹏﹋﹌︴﹟#﹩$﹠&﹪%*﹡﹢﹦﹤‐￣¯―﹨ˆ˜﹍﹎+=' \
                        '<＿_-\ˇ~﹉﹊（）〈〉‹›﹛﹜『』〖〗［］《》〔〕{}「」【】︵︷︿　' \
                        '︹︽_﹁﹃︻︶︸﹀︺︾ˉ﹂﹄︼❝❞'
    for special_char in special_chars:
        s = s.replace(special_char, ' ')
    return s


def attach(japanese, romaji):
    '''

    japanese -> word_romaji_list -> word_kana_list
    romaji -> kana
    unmatched_kana = kana
    result = ''
    for every word in word_kana_list:
        kanas = word_kana_list[word_index]
        for every kana in kanas:
            if front_match(kana, unmatched_kana):
                remove kana in unmatched_kana
                result += word + '(' + kana + ')'
                break
    return result
    '''
    # pre process
    japanese = remove_speical_chars(japanese)
    japanese = japanese.replace('ァ', 'あ')

    # japanese -> word_romaji_list -> word_kana_list
    word_kana_list = get_sentence_kana(d, japanese, c)

    # romaji -> kana
    kana = romaji2kana(fifty, romaji)
    unmatched_kana = deepcopy(kana)
    result = ''

    # main loop
    for i in range(len(word_kana_list)):
        word = word_kana_list[i][0]
        kanas = word_kana_list[i][1]
        is_matched = False
        for kana in kanas:
            if front_match(unmatched_kana, kana):
                unmatched_kana = remove_front(unmatched_kana, kana)
                kana = remove_front_same_part(word, kana)
                result += word + '(' + kana + ')'
                is_matched = True
                break
        if not is_matched:
            result += '未完成匹配'
            break
    # post process
    result = result.replace('()', '')
    return result


def attach_v2(japanese, romaji):
    # pre process
    japanese = remove_speical_chars(japanese)
    japanese = japanese.replace('ァ', 'あ')

    # japanese -> word_romaji_list -> word_kana_list
    word_kana_list = get_sentence_kana(d, japanese, c)
    choices = dfs_list_in_list(word_kana_list)

    # romaji -> kana
    kana = romaji2kana(fifty, romaji)
    result = ''

    if debug:
        print(choices)
        print(kana)

    for choice in choices:
        (key, value), = choice.items()
        if equal(kana, key):
            result = value
            break

    # post process
    result = result.replace('()', '')
    if result == '':
        result = japanese + ' 匹配失败'
    return result


def equal(s1: str, s2: str):
    # equal means s1 is the same with s2, except は and わ
    same_voice_list =[
        ['は', 'わ'], ['じ', 'ぢ'], ['ず', 'づ'], ['や', 'ゃ'], ['ー', 'え'],
        ['へ', 'え']
    ]
    if len(s1) != len(s2):
        return False
    if len(s1) == 0:
        return True
    for i in range(len(s1)):
        if s1[i] == s2[i]:
            continue
        is_same_voice = False
        for same_voice in same_voice_list:
            if s1[i] in same_voice and s2[i] in same_voice:
                is_same_voice = True
                break
        if is_same_voice:
            continue
        else:
            return False
    return True


def label_kana(word, kana):
    result = ''
    # remove front
    kana = remove_front_same_part(word, kana)

    # remove back
    i = len(word) - 1
    j = len(kana) - 1
    if i > 0 and j > 0 and word[i] == kana[j]:
        while 1:
            if word[i] != kana[j]:
                break
            i -= 1
            j -= 1
        i += 1
        j += 1
        result = word[:i] + '(' + kana[:j] + ')' + word[i:]
    else:
        result = word + '(' + kana + ')'
    return result


def dfs_list_in_list(l: list):
    result = []
    if len(l) == 1:
        for e in l[0][1]:
            result.append({e: label_kana(l[0][0], e)})
        return result
    for e in l[0][1]:
        com_list = dfs_list_in_list(l[1:])
        for com in com_list:
            (key, value), = com.items()
            result.append({e + key: label_kana(l[0][0], e) + value})
    return result


if __name__ == '__main__':
    fifty = get_fifty('五十音图.txt')
    if debug:
        a = attach_v2('屍を積み上げふいに我にかえるたび',
                      'Shikabane wo tsumiage fui ni warani kaeru tabi')
        print(a)
    else:
        input_file = open(args.input, 'r', encoding='utf-8')
        content = input_file.read().split('\n')
        input_file.close()

        output_file = open(args.output, 'w', encoding='utf-8')

        japanese = ''
        romaji = ''

        for line in content:
            line_type = get_sentence_type(line)
            if line_type == 'japanese':
                japanese = line
            elif line_type == 'romaji':
                romaji = line
            else:
                continue
            if japanese != '' and romaji != '':
                r = attach_v2(japanese, romaji)
                output_file.write(r + '\n' + romaji + '\n')
                japanese = ''
                romaji = ''

        output_file.close()