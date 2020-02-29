# coding:utf-8

import socket
from urllib import parse
import threading
from frontend import get_index
from backend import *
from queue import Queue
import time


class HTTPServer(object):
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.url_queue = Queue() # 输入的URL队列
        self.output_dict = {} # 输出的字典，key是socket，value是romajis
        translate_thread = threading.Thread(target=self.translate_thread_func)
        translate_thread.setDaemon(True)
        translate_thread.start()

    def start(self):
        self.server_socket.listen(128)
        print('Done.Waiting for connections...')
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(client_address[0])
            handle_client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            handle_client_thread.setDaemon(True)
            handle_client_thread.start()

    def handle_client(self, client_socket):
        """
        处理客户端请求
        """
        # 获取客户端请求数据
        request_data = client_socket.recv(5000)
        request_data = str(request_data, 'utf-8').split('\r\n')[0]
        request_data = request_data.split(' ')
        if len(request_data) < 2:
            client_socket.close()
            return

        method = request_data[0]
        content = parse.unquote(request_data[1])
        if method != 'GET':
            client_socket.close()
        self.resolve_request(content, client_socket)

    def response(self, content_html, socket):
        # 构造响应数据
        response_start_line = "HTTP/1.1 200 OK\r\n"
        response_headers = '\r\n\r\n'
        response_body = '<!DOCTYPE html><html><body>' \
                        '<head><meta charset="UTF-8"/><title>罗马音机翻</title></head>' + content_html + '</body>'
        response = response_start_line + response_headers + response_body + '</html>'

        # 向客户端返回响应数据
        socket.send(bytes(response, "utf-8"))
        # 关闭客户端连接
        socket.close()

    def bind(self, port):
        self.server_socket.bind(("", port))

    def is_legal(self, keyword):
        illegal_words = ['', '-', '机翻', '-机翻', '-机', '翻']
        if keyword in illegal_words:
            return False
        return True

    def resolve_request(self, request_content, socket):
        result_html = ''
        if request_content == '/':
            result_html = get_index()
        elif 'translate?url=' in request_content:
            # 获取url和翻译类型 放进输入队列
            resultType = request_content[request_content.find('type=') + 5]
            result_html = get_index(is_index=False)
            url = request_content[request_content.find('translate?url=') + 14:]
            self.url_queue.put([socket, url, resultType])
            # 等待输出字典里面有输出
            while 1:
                if socket in self.output_dict.keys():
                    translate_result = self.output_dict[socket]
                    break
                time.sleep(1)

            if not self.is_legal(url) or len(translate_result) == 0:
                result_html += '<h1 style="text-align:center">没有找到' + url + '</h1>'
                result_html += '<p style="text-align:center"><a href="https://item.taobao.com/item.htm?' \
                               'spm=a230r.1.14.22.74443d957TgCNh&id=602883109035&' \
                               'ns=1&abbucket=9#detail"' \
                               'style="font-size:22px;color:red">专业日语歌标注罗马音：10元/首</a></p>'

            for line in translate_result:
                result_html += '<p style="text-align:center;font-weight:bold">' + line + '</p>' + '\r\n'

        elif '/favicon.ico' in request_content:
            pass
        else:
            print('未知的请求类型:', request_content)

        self.response(result_html, socket)

    def translate_thread_func(self):
        while 1:
            socket, url, resultType = self.url_queue.get()
            translate_result = self.translate(url, resultType)
            self.output_dict[socket] = translate_result

    def translate(self, url, resultType):
        if 'http' == url[0:4]:
            lrc = get_lrc_from_netease_url(url)
        else:
            lrc = get_lrc_from_lrc_str(url)
        if lrc is None or len(lrc) == 0:
            return ['没有找到歌词', '请确认输入是否正确']
        romajis = get_romaji(lrc)

        for i in range(len(romajis)):
            romajis[i] = seperate_a_romaji(romajis[i])

        if resultType == '2':
            romajis = romaji_to_pinyin(romajis)

        results = []
        for i in range(len(lrc)):
            results.append(lrc[i])
            romajis[i] = romajis[i].replace('-', '')
            results.append(romajis[i])

        return results


def main():
    # start server
    http_server = HTTPServer()
    http_server.bind(9000)
    http_server.start()


if __name__ == "__main__":
    main()
