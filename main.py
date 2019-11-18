import argparse
from backend import *


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
if args.separate:
    romajis = separate_romajis(romajis)
if args.pinyin:
    if not args.separate:
        romajis = separate_romajis(romajis)
    romajis = romaji_to_pinyin(romajis)

if args.output:
    file = open(args.output, 'w', encoding='utf-8')
    for i in range(len(lrc)):
        file.write(lrc[i] + '\n')
        file.write(romajis[i] + '\n')
    file.close()
    print('romajis saved in', args.output)
else:
    # display
    print('-----------------------------------------')
    for i in range(len(lrc)):
        print(lrc[i])
        print(romajis[i])

