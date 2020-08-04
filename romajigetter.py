#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
from copy import deepcopy


class RomajierGetter:

    def page_loading_timeout(self, driver, url, timeout):
        driver.set_page_load_timeout(timeout)
        try:
            driver.get(url)
        except:
            driver.execute_script("window.stop()")

    def __init__(self):
        chrome_opt = Options()      # 创建参数设置对象.
        chrome_opt.add_argument('--no-sandbox')
        chrome_opt.add_argument('--headless')   # 无界面化.
        chrome_opt.add_argument('--disable-gpu')    # 配合上面的无界面化.
        # chrome_opt.add_argument('--window-size=1366,768')   # 设置窗口大小, 窗口大小会有影响.
        # 创建Chrome对象并传入设置信息.
        self.driver = webdriver.Chrome(chrome_options=chrome_opt)

        # driver.set_page_load_timeout(100)
        # 操作这个对象.
        print('Waiting for google translate...')
        self.driver.get('https://translate.google.cn/#view=home&op=translate&sl=ja&tl=en')
        # self.page_loading_timeout(self.driver, 'https://translate.google.cn/', 6)

        self.input_object = self.driver.find_element_by_id('source')
        self.correction_object = self.driver.find_element_by_xpath('//*[@id="spelling-correction"]')
        #self.exchange_button = self.driver.find_element_by_xpath(
        #        '/html/body/div[2]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[3]/div')

        if self.input_object is None:
            print('ERROR: cannot find textarea')
            exit()
        self.output_object = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/div/div/div[3]/div[1]')
        if self.output_object is None:
            print('ERROR:cannot find output element')
            exit()
        if self.correction_object is None:
            print('ERROR: cannot find correction object')
            exit()
        # if self.exchange_button is None:
        #     print('ERROR: cannot find exchange button')
        #     exit()
        print('Google translate ready.Putting in lrc...')

    def refresh(self):
        self.driver.refresh()
        self.input_object = self.driver.find_element_by_id('source')
        self.correction_object = self.driver.find_element_by_xpath('//*[@id="spelling-correction"]')
        self.output_object = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/div/div/div[3]/div[1]')

    def random_sleep(self, min_val, max_val):
        sleep_time = min_val + random.random() * (max_val - min_val)
        time.sleep(sleep_time)
        return sleep_time

    def get_romaji(self, sentence):
        self.input_object.clear() # 首先清空输入框
        while self.output_object.text != '':  # 等待清空操作完成
            time.sleep(1)
        self.input_object.send_keys(sentence)  # 把句子填进去

        time_threshold = 5
        time_past = 0
        romaji = ''
        while romaji == '':  # 等待出结果
            sleep_time = self.random_sleep(1, 2)
            time_past += sleep_time # 记录流逝时间
            if time_past > time_threshold: # 如果卡了，点击两次交换语言
                # self.exchange_button.click()
                self.random_sleep(1, 2)
                # self.exchange_button.click()
                time_past = 0
            romaji = self.output_object.text
            # 万一不是日语的话
            if '源语言' in self.correction_object.text:
                return '不是日语哦'
            else:
                print(self.correction_object.text)

        # 自动纠错
        correction_status = self.correction_object.value_of_css_property('display')
        if correction_status != 'none':  # 如果有纠错提示
            correction_ab = self.driver.find_element_by_xpath('//*[@id="spelling-correction"]/a/b')  # 找到纠错内容
            new_sentence = correction_ab.text
            self.input_object.clear()  # 首先清空输入框
            while self.output_object.text != '':  # 等待清空操作完成
                time.sleep(1)
            self.input_object.send_keys(new_sentence)  # 把新句子填进去
            romaji = ''
            while romaji == '':  # 等待出结果
                self.random_sleep(1, 2)
                romaji = self.output_object.text
        return romaji

    def replace_o_with_wo(self, sentence):
        # 三种情况，前后都是空格，第一个是o第二个是空格，最后一个是o，倒数第二个是空格
        result = deepcopy(sentence)
        result = result.replace(' o ', ' wo ')
        if len(result) >= 2 and result[0] == 'O' and result[1] == ' ':
            result = 'Wo' + result[1:]
        if len(result) >= 2 and result[-1] == 'o' and result[-2] == ' ':
            result = result[:-1] + 'wo'
        return result

    def get_multi_sentences_romaji(self, sentences):
        print('Getting romajis...')
        sentences_str = ''
        for sentence in sentences:
            sentences_str += sentence + '|'
        sentences_str = sentences_str[:-1] # 去掉最后一个|
        romaji_str = self.get_romaji(sentences_str)
        romajis = romaji_str.split('|')
        for i in range(len(romajis)):
            romajis[i] = romajis[i].strip().capitalize()
        # 去掉没用的字符
        for i in range(len(romajis)):
            romajis[i] = romajis[i].replace('-', ' ')
            romajis[i] = romajis[i].replace('`', '')
            romajis[i] = romajis[i].replace('dzu', 'zu')
            romajis[i] = romajis[i].replace('tchi', 'chi')
            romajis[i] = romajis[i].replace('ā', 'a')
            romajis[i] = romajis[i].replace('ē', 'e')
            romajis[i] = romajis[i].replace('ō', 'ou')
            romajis[i] = romajis[i].replace('ū', 'uu')
            romajis[i] = romajis[i].replace('ī', 'ii')
            romajis[i] = romajis[i].replace('\r\n\r\n', '\r\n')
            romajis[i] = romajis[i].replace('\'', '')
            romajis[i] = self.replace_o_with_wo(romajis[i])
            romajis[i] = romajis[i].capitalize()
        print('Done')
        return romajis

    def quit(self):
        self.driver.quit()


if __name__ == '__main__':
    romajier = RomajierGetter()
    romajier.replace_o_with_wo()



