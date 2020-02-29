# -*- coding:utf-8 -*-
import requests
import json
import re


class LyricsGetter:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
        }
        cookie = '_iuqxldmzr_=32; _ntes_nnid=e1140ebd82c21989a45988e0a0b0848f,1568210409344; _ntes_nuid=e1140ebd82c21989a45988e0a0b0848f; WM_TID=ekgG3ovD%2Bm9FVFVEEENt8xxU0v%2BsELca; WM_NI=6MoRS2Js%2FgvO3hkX6nOoPrBZXgfdNg%2BcVX0xrKsWePYz%2Bxmfk2lSjRbRKEzPULt9Jqo7pzNi3Zu1kan2uIfxSQTD3uEXdm1x6g7U1d43dF5tup1af6m63ukuFIj51cPARlM%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee84e667f5afa9b0d253908e8aa6c45e828b9e84f33fa5e787d6fb4dfb92a8b9d92af0fea7c3b92af693a1b3d23a8aade188f545f1b8a5b9b5668db1a093c1529cb9aa85cd6de9bd9ab9b374b295bdb8e85c9ba6e599f06ea9eea4b4e95aa28e85a6f95c9794bcdac97bade9c09bcd63f186bbd2ea6baeeebbaae574918f9ca5b27f8788ac8eb474f6b9f9b6b470f8edaca7b880b7b0ff82e53eafeafd96ea7f8697a6d6b469949f9e8dd037e2a3; hb_MA-BFF5-63705950A31C_source=www.baidu.com; JSESSIONID-WYYY=9t9Uj4eqoKAT6XJ1Tdiz9iqIzSvwNEJ16g8HEkVtPrT5PElWPR0bWS%2FcEGdi2FZSCORcZ8mQoBU%2FQjCkJY741%5CjjjTqmTJwOjO9gRDpO3l7Vj4bTBu%5CWMfofxFd1d%5CkBGWlX%2FPgV9QhBPjAOftTKYvSpjacG8s219%2B7Yq5%2Bl9JBnjzNR%3A1568554054768'
        self.cookie_dict = {i.split("=")[0]: i.split("=")[-1] for i in cookie.split("; ")}
    def get_lyrics_from_id(self, id):
        lrc_url = 'http://music.163.com/api/song/lyric?' + 'id=' + id + '&lv=1&kv=1&tv=-1'

        lyric = requests.get(lrc_url, headers=self.headers, cookies=self.cookie_dict)
        json_obj = lyric.text
        j = json.loads(json_obj)
        if 'lrc' in j.keys():
            lrc = j['lrc']['lyric']
            pat = re.compile(r'\[.*\]')
            lrc = re.sub(pat, "", lrc)
            lrc = lrc.strip()
            lrc = lrc.split('\n')
            return lrc
        else:
            return None

    def get_name_singer_from_url(self, url):
        result = requests.get(url, headers=self.headers, cookies=self.cookie_dict).text
        print(result)
        result = result.split('title')[1]
        result = result[1:]
        result = result[: result.find(' - 单曲 - 网易云音乐')]
        return result

    def get_lyrics_from_url(self, url):
        start = url.find('id=')
        end = url.find('&userid')
        if end == -1:
            id = url[start + 3:]
        else:
            id = url[start + 3: end]
        # name_singer = self.get_name_singer_from_url(url)
        return self.get_lyrics_from_id(id)

    def get_song_list_from_url(self, url):
        result = requests.get(url, headers=self.headers, cookies=self.cookie_dict).text
        result = result.split('<li>')[1:]
        ids = []
        song_names = []
        for item in result:
            if 'song?id=' in item:
                start = item.find('song?id=')
                end = item.find('">')
                id = item[start + 8: end]
                if id != '${song.id}' and id != '':
                    ids.append(id)
                    song_name = item[end + 2: item.find('</a>')]
                    song_names.append(song_name)
        print('Totally', len(ids), 'songs')
        return ids, song_names

if __name__ == '__main__':
    lyric_getter = LyricsGetter()
    lrc = lyric_getter.get_lyrics_from_url(
                'https://music.163.com/song?id=34040109&userid=398697337')
    print(lrc)
    # print(name_singer)
    # lyric_getter.get_song_list_from_url(
    #                    'https://music.163.com/playlist?id=2665979377')
