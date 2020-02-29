import argparse
from backend import *


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='The input file')
parser.add_argument('output_path')

args = parser.parse_args()

input_file = open(args.input, 'r', encoding='utf-8')
content = input_file.read().split('\n')
input_file.close()
content = separate_romajis(content)

output_file = open(args.output_path, 'w', encoding='utf-8')
for line in content:
    output_file.write(line + '\n')
output_file.close()