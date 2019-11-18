# coding=utf-8
from romajigetter import RomajierGetter
from lyrics_getter import LyricsGetter
from copy import deepcopy


def get_romaji(sentences):
    romajier = RomajierGetter()
    romajis = romajier.get_multi_sentences_romaji(sentences)
    romajier.quit()
    return romajis


def get_lrc_from_netease_url(url):
    print('Getting lrc from url:', url)
    lyric_getter = LyricsGetter()
    sentences = lyric_getter.get_lyrics_from_url(url)
    print('Lrc done')
    return sentences


def get_lrc_from_txt_file(path):
    print('Getting lrc from local file:', path)
    file = open(path, 'r', encoding='utf-8')
    content = file.read()
    lrc = get_lrc_from_lrc_str(content)
    file.close()
    print('Lrc done')
    return lrc


def get_lrc_from_lrc_str(lrc_str):
    sentences = lrc_str.split('\n')
    for i in range(len(sentences)):
        sentences[i] = sentences[i].replace('\r', '')
    return sentences


def separate_a_romaji(romaji):
    result = ''
    vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U', 'ī', 'ō', 'ū']
    i = 0
    while 1:
        if i > len(romaji) - 1:
            break
        for j in range(10):
            if i + j > len(romaji) - 1:
                i = i + j + 1
                break
            if romaji[i + j] == 'n' and i + j + 1 < len(romaji) and \
                    romaji[i + j + 1] not in vowels and romaji[i + j + 1] != 'y':
                result += 'n' + ' '
                i = i + j + 1
                break
            if romaji[i + j] in vowels:
                result += romaji[i:i + j + 1] + ' '
                i = i + j + 1
                break
    if len(romaji) > 0 and romaji[-1] == 'n':
        result += 'n'
    return result


def separate_romajis(romajis):
    print('Separating romajis...')
    result = deepcopy(romajis)
    for i in range(len(result)):
        result[i] = separate_a_romaji(result[i])
    print('Done')
    return result


def romaji_to_pinyin(romajis):
    pinyin = deepcopy(romajis)
    for i in range(len(pinyin)):
        pinyin[i] = str(pinyin[i]).lower()
        pieces = pinyin[i].split(' ')
        temp = ''
        for piece in pieces:
            if piece == 'i' or piece == 'ī':
                piece = 'yi'
            if piece == 'u':
                piece = 'wu'
            if piece == 'o':
                piece = 'wo'
            if piece == 'e':
                piece = 'ei'
            if piece == 'tsu':
                piece = 'cu'
            if piece == 'shi':
                piece = 'xi'
            if piece == 'sha':
                piece = 'xia'
            if piece == 'sho':
                piece = 'xiu'
            if piece == 'chi':
                piece = 'qi'
            if piece == 'dzu':
                piece = 'zu'
            if piece == 'ju':
                piece = 'jou'
            if len(piece) == 2 and piece[0] == 'r':
                piece = 'l' + piece[1]
            if len(piece) > 1 and piece[-1] == 'o' and piece[0] != 'w':
                piece = piece + 'u'
            if len(piece) >= 3 and piece[0] == piece[1]:
                piece = piece[0] + piece[2]
            if len(piece) > 1 and piece[-1] == 'e':
                piece = piece + 'i'
            if len(piece) > 1 and piece[-1] == 'ō':
                piece = piece[:-1] + 'oo'
            if len(piece) > 1 and piece[-1] == 'ū':
                piece = piece[:-1] + 'uu'
            if len(piece) > 1 and piece[-1] == 'ī':
                piece = piece[:-1] + 'ii'
            piece += ' '
            temp += piece
        pinyin[i] = temp
        if len(pinyin[i]) >= 2:
            pinyin[i] = pinyin[i][0].upper() + pinyin[i][1:]
    return pinyin