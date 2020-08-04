def is_alpha(c):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    return c in alphabet


def has_space_char(romaji):
    for i in range(len(romaji) - 1):
        if romaji[i] == ' ' and not is_alpha(romaji[i + 1]):
            return True
    return False


def separate_a_romaji(romaji):
    result = ''
    vowels = ['a', 'e', 'i', 'ē', 'o', 'u', 'A', 'E', 'I', 'O', 'U', 'ī', 'ō', 'ū']

    i = 0
    while 1:
        if i > len(romaji) - 1:
            break
        for j in range(10):
            if i + j > len(romaji) - 1:
                i = i + j + 1
                break
            elif romaji[i + j] in vowels:
                result += romaji[i:i + j + 1]
                if i + j + 1 < len(romaji) and romaji[i + j + 1] not in vowels:
                    result += ' '
                i = i + j + 1
                break
            if not is_alpha(romaji[i + j]):
                result += romaji[i:i + j + 1]
                i = i + j + 1
                break
    # n
    result = list(result)
    if len(result) > 1:
        for i in range(1, len(result) - 1):
            if result[i - 1] == ' ' and result[i] == 'n' and result[i + 1] not in vowels:
                result[i - 1] = 'n'
                result[i] = ' '
    result = ''.join(result)
    while has_space_char(result):
        for i in range(len(result) - 1):
            if result[i] == ' ' and not is_alpha(result[i + 1]):
                result = result[:i] + result[i + 1:]
                break

    return result


if __name__ == '__main__':
    print(separate_a_romaji('konoyome'))