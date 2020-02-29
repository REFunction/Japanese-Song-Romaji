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
    sentence = separate_a_romaji(sentence)
    romajis = sentence.split(' ')

    print(romajis)

    result = ''
    for romaji in romajis:
        if len(romaji) >= 3 and romaji[0] == romaji[1]:
            result += 'っ'
            romaji = romaji[1:]
        result += fifty[romaji]

    return result


if __name__ == '__main__':
    fifty = get_fifty('五十音图.txt')
    while 1:
        s = input('>')
        kana = romaji2kana(fifty, s)
        print(kana)