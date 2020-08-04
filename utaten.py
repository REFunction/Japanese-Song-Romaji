import requests
from pykakasi import kakasi
from bs4 import BeautifulSoup
from backend import is_alpha


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


def get_html(url):
    response = requests.get(url)
    return response.text


def remove_others(s):
    line = str(s).replace('<html><body>', '')
    line = line.replace('</body></html>', '')
    line = line.replace('<p>', '')
    line = line.replace('</p>', '')
    line = line.replace('<div class="hiragana">', '')
    line = line.replace('<div class="romaji" style="display: none;">\n', '')
    line = line.replace('</div>', '')
    return line


def remove_not_alpha(romaji):
    result = ''
    for c in romaji:
        if is_alpha(c) or c == ' ':
            result += c
    return result


def get_lyric(url, mode='hiragana'):
    '''
    :param url:
    :param mode: 'hiragana' or 'romaji'
    :return:
    '''
    html = requests.get(url).text
    html = BeautifulSoup(html, features='lxml')
    if mode == 'hiragana':
        html = str(html.select('.hiragana')[0])
    elif mode == 'romaji':
        html = str(html.select('.hiragana')[0])
    else:
        print('Unknown mode:', mode)
        exit()

    result = []

    html = html.split('<br/>')
    for line in html:
        # if 'それがすべてさ' in line:
        #     print(line)

        line = BeautifulSoup(line, features='lxml')
        rubies = line.select('.ruby')
        src = str(line)
        for ruby in rubies:
            ruby = str(ruby)
            ruby = BeautifulSoup(ruby, features='lxml')
            rb = str(ruby.select('.rb'))
            rb = get_content_between(rb, '<span class="rb">', '</span>')
            rt = str(ruby.select('.rt'))
            rt = get_content_between(rt, '<span class="rt">', '</span>')

            ruby = str(ruby)
            ruby = ruby.replace('<html><body>', '')
            ruby = ruby.replace('</body></html>', '')
            if mode == 'hiragana':
                line = str(line).replace(str(ruby), rb + '(' + rt + ')')
                result.append(line)
            else:
                src = str(line).replace(str(ruby), rb)
                line = str(line).replace(str(ruby), rt + ' ')
            if len(line) != 1:
                line = line.replace('\n', '')

        line = remove_others(line)
        src = remove_others(src)
        if mode == 'romaji':
            # post processing
            line = conv.do(line)
            line = remove_not_alpha(line)
            line = line.replace('  ', ' ')
            if len(line) > 1:
                line = line[0].upper() + line[1:]
            result.append(src + '\n' + line)
        else:
            result.append(line)

    return result


if __name__ == '__main__':
    k = kakasi()
    k.setMode('H', 'a')
    k.setMode('K', 'a')
    k.setMode('J', 'a')
    conv = k.getConverter()

    url = 'https://utaten.com/lyric/iz18101814/'
    lrc = get_lyric(url, mode='romaji')
    for line in lrc:
        if line == '\n':
            print()
        else:
            print(line)
