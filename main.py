import argparse
from backend import *
from yahoo import get_romajis


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help='netease url')
parser.add_argument('-p', '--path', help='local file path')
parser.add_argument('-o', '--output', help='output file path')
parser.add_argument('-s', '--separate', action="store_true", help='if separate a romaji')
parser.add_argument('-pi', '--pinyin', action="store_true", help='if pinyin')
args = parser.parse_args()

lrc = None

if args.url:
    lrc = get_lrc_from_netease_url(args.url)
elif args.path:
    lrc = get_lrc_from_txt_file(args.path)
else:
    print('You must provide a url or a local path.')
    exit()

if lrc is None or len(lrc) == 0:
    print('Cannot get lrc. Make sure your url or path.')
    exit()

romajis = get_romaji(lrc)
# romajis = get_romajis(lrc)
name_singer = ''
if args.separate:
    romajis = separate_romajis(romajis)
if args.pinyin:
    if not args.separate:
        romajis = separate_romajis(romajis)
    romajis = romaji_to_pinyin(romajis)

if args.output:
    file = open(args.output, 'w', encoding='utf-8')
elif args.url:
    name_singer = get_name_singer_from_url(args.url)
    file = open(name_singer + '.txt', 'w', encoding='utf-8')

else:
    file = open('output.txt', 'w', encoding='utf-8')
result = ''
for i in range(len(lrc)):
    result += lrc[i] + '\n'
    result += romajis[i] + '\n'
result = result.replace('\n\n', '\n')
if len(result) >= 1 and result[-1] == '\n':
    result = result[:-1]
file.write(result)
file.close()

if args.output:
    print('romajis saved in', args.output)
elif args.url:
    print('romajis saved in', name_singer + '.txt')
else:
    print('romajis saved in output.txt')