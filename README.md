# Japanese-Song-Romaji
The fastest way to know how to sing a Japanese song in the world.
## Requirements
### 1.python packages
- selenium
- requests
- langid
### 2.chrome (browser)
#### for windows
Download from [here](https://www.google.cn/intl/zh-CN/chrome/)
#### for ubuntu
sudo wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome*
### 3.chromedriver
Download from [here](http://npm.taobao.org/mirrors/chromedriver/)

Make sure it is in your environment variables.

The version must be the same with your chrome.
## usage
```
main.py [-h] [-u URL] [-p PATH] [-o OUTPUT] [-s] [-pi]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     netease url
  -p PATH, --path PATH  local file path
  -o OUTPUT, --output OUTPUT
                        output file path
  -s, --separate        if separate a romaji
  -pi, --pinyin         if pinyin
```

### demo
- For netease cloud music
```
python3 main.py -u "https://music.163.com/song?id=1350081368"
```
- For local lrc file
```
python3 main.py -p input.txt
```