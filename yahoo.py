from bs4 import BeautifulSoup
from pykakasi import kakasi
import requests
from copy import deepcopy
import urllib.parse
from tqdm import trange


def get_conv():
    k = kakasi()
    k.setMode('H', 'a')
    k.setMode('K', 'a')
    k.setMode('J', 'a')
    conv = k.getConverter()
    return conv


def get_content_between(content, start_word=None, end_word=None):
    start = 0
    end = len(content)
    if start_word:
        start = content.find(start_word)
    if end_word:
        end = content.find(end_word)
    if start_word:
        return content[start + len(start_word): end]
    else:
        return content[start: end]


def is_alpha(c):
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return c in alphabet


def remove_not_alpha(s):
    result = ''
    for c in s:
        if is_alpha(c) or c == ' ':
            result += c
    while len(result) >= 1 and result[0] == ' ':
        result = result[1:]
    if len(result) >= 1:
        result = result[0].upper() + result[1:]
    elif len(result) == 1:
        result = result[0].upper()
    while '  ' in result:
        result = result.replace('  ', ' ')
    return result


def get_romaji_from_ja(sentences):
    conv = get_conv()
    appid = 'dj00aiZpPUFzd3FmWEoyV012ZSZzPWNvbnN1bWVyc2VjcmV0Jng9YTI-'
    base_url = 'https://jlp.yahooapis.jp/MAService/V1/parse?appid=' + appid + \
               '&results=ma&uniq_filter=9%7C10&sentence='

    request_content = ''
    for s in sentences:
        request_content += s + '|'
    request_content = request_content[:-1]

    url = base_url + urllib.parse.quote(request_content)
    html = requests.get(url, timeout=20).text
    html = BeautifulSoup(html, features='lxml')
    words = html.find_all('word')
    romaji = ''
    for word in words:
        word = str(word)
        word = BeautifulSoup(word, features='lxml')
        surface = str(word.find('surface'))
        reading = str(word.find('reading'))
        surface = get_content_between(surface, '<surface>', '</surface>')
        reading = get_content_between(reading, '<reading>', '</reading>')
        reading = conv.do(reading)
        romaji += reading + ' '

    romajis = romaji.split('|')
    for i in range(len(romajis)):
        romajis[i] = remove_not_alpha(romajis[i])
        if len(romajis[i]) >= 1 and romajis[i][-1] == ' ':
            romajis[i] = romajis[i][:-1]
            romajis[i] = replace_ha_with_wa(romajis[i])

    return romajis


def get_romajis(sentences):
    if len(sentences) < 10:
        return get_romaji_from_ja(sentences)
    romajis = []
    for i in trange(0, len(sentences), 10):
        batch = sentences[i: min(i + 10, len(sentences))]
        romaji_batch = get_romaji_from_ja(batch)
        for romaji in romaji_batch:
            romajis.append(romaji)
    return romajis


def replace_ha_with_wa(sentence):
    # 三种情况，前后都是空格，第一个是Ha第二个是空格，最后一个是ha，倒数第二个是空格
    result = deepcopy(sentence)
    result = result.replace(' ha ', ' wa ')
    if len(result) >= 3 and result[0] == 'H' and result[1] == 'a' and result[2] == ' ':
        result = 'Wa' + result[2:]
    if len(result) >= 3 and result[-1] == 'a' and result[-2] == 'h' and result[-3] == ' ':
        result = result[:-2] + 'wa'
    return result


if __name__ == '__main__':
    r = get_romaji_from_ja(['失う不安で怖かったんだ'])
    print(r)