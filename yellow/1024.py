import requests
import threading
import re
import os


class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, url, dir, filename):
        threading.Thread.__init__(self)
        self.threadID = filename
        self.url = url
        self.dir = dir
        self.filename = filename

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        download_pic(self.url, self.dir, self.filename)


def download_pic(url, dir, filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name',
        'Referer': 'https://t66y.com'}
    req = requests.get(url=url, headers=headers)
    if req.status_code == 200:
        with open(str(dir) + '/' + str(filename) + '.jpg', 'wb') as f:
            f.write(req.content)


try:
    flag = 1
    while flag <= 270:
        base_url = 'https://t66y.com/'
        page_url = 'https://t66y.com/thread0806.php?fid=8&search=&page=' + str(flag)
        get = requests.get(page_url)
        article_url = re.findall(r'<h3><a href="(.*)" target="_blank" id="">(?!<.*>).*</a></h3>',
                                 str(get.content, 'gbk', errors='ignore'))
        for url in article_url:
            threads = []
            tittle = ['default']
            getpage = requests.get(str(base_url) + str(url))
            tittle = re.findall(r'<h4>(.*)</h4>', str(getpage.content, 'gbk', errors='ignore'))
            file = tit# -*- coding=utf-8 -*-
import requests
import random
import os
import threading
from bs4 import BeautifulSoup

proxies = {
  "http": "http://127.0.0.1:1087",
  "https": "http://127.0.0.1:1087",
}
UserAgent = [
    "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-N976V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.89 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SAMSUNG SM-G977N Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/9.2 Chrome/67.0.3396.87 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.83 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SAMSUNG SM-F900U Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/9.2 Chrome/67.0.3396.87 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-A805F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.112 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-A505F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.105 Mobile Safari/537.36"
]


class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, title, img_url, num):
        threading.Thread.__init__(self)
        self.title = title
        self.img_url = img_url
        self.num = num

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        download_img(self.title, self.img_url, self.num)


def download_html(page_num):
    url = "http://www.t66y.com/thread0806.php?fid=16&search=&page={}".format(page_num)
    headers = {
        "User-Agent": "{}".format(random.choice(UserAgent))
    }
    response = requests.request("GET", url, headers=headers)
    response.encoding = 'gbk'
    return response.text


def get_page_url(html):
    soup = BeautifulSoup(html, 'lxml')
    h3 = soup.find_all('h3')
    page_url = []
    for i in h3:
        if 'htm_data' in i.a['href'] and 'P]' in i.a.string:
            page_url.append([i.a['href'], i.a.string])
        else:
            pass
    return page_url


def download_img(title, img_url, num):
    headers = {
        "User-Agent": "{}".format(random.choice(UserAgent))
    }
    response = requests.request("GET", img_url, headers=headers)
    if response.status_code == 200:
        with open("{}/img/{}/{}.jpg".format(os.getcwd(), title, num), 'wb') as f:
            f.write(response.content)
        f.close()


def get_img_url(i):
    page_url = i[0]
    page_name = i[1]
    threads = []

    if os.path.exists("{}/img/{}".format(os.getcwd(), page_name)) is False:
        os.makedirs("{}/img/{}".format(os.getcwd(), page_name))

    url = "http://www.t66y.com/" + str(page_url)
    headers = {
        "User-Agent": "{}".format(random.choice(UserAgent))
    }
    response = requests.request("GET", url, headers=headers)
    response.encoding = 'gbk'
    soup = BeautifulSoup(response.text, 'lxml')
    img_urls = soup.find_all('img')
    for j in range(len(img_urls)):
        if "ess-data" in img_urls[j].attrs:
            print(page_name, img_urls[j]['ess-data'])
            thread = myThread(page_name, img_urls[j]['ess-data'], j)
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)
    for t in threads:
        t.join()


def main():
    page_num = 1
    while page_num <= 100:
        html = download_html(page_num)
        page_urls = get_page_url(html)
        for i in page_urls:
            get_img_url(i)
        page_num += 1


if __name__ == '__main__':
    main()

tle[0]
            if os.path.exists(file) == False:
                os.makedirs(file)
                img_url = re.findall(r'<input src=\'(.*?)\'', str(getpage.content, 'gbk', errors='ignore'))
                filename = 1
                print('开始下载：' + file)
                for download_url in img_url:
                    thread = myThread(download_url, file, filename)
                    thread.start()
                    threads.append(thread)
                    filename = filename + 1
                for t in threads:
                    t.join()
                print('下载完成，共' + str(filename) + '张图片')
            else:
                print('文件夹已存在，跳过')
        print('第' + str(flag) + '页下载完成')
        flag = flag + 1
except:
    print('程序错误，退出')
