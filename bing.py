import os
import requests
from requests.exceptions import RequestException
# from urllib.parse import urlencode
from hashlib import md5
from multiprocessing.pool import Pool
from pyquery import PyQuery as pq
# import time
import re

GROUP_START = 1
GROUP_END = 10


def get_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def get_images_url(html):
    doc = pq(html)
    cards = doc('.item .card').items()
    for item in cards:
        # name = re.sub('\(.*?\)|（.*?）', '', item.find('.location .t').text())
        name = item.find('.location .t').text()
        yield {
            "name": name,
            "url": item.find('img').attr('src').replace('400x240', '1920x1080')
        }


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
}


def save_images(img):
    if not os.path.exists('images'):
        os.mkdir('images')
    try:
        response = requests.get(img.get('url'), headers=headers)
        if response.status_code == 200:
            file_path = img.get('name') + md5(response.content).hexdigest() + '.jpg'
            print(file_path)
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('failed to save image')


def main(page):
    url = 'https://bing.ioliu.cn/ranking?p=' + str(page)
    html = get_page(url)
    lis = get_images_url(html)
    os.chdir('images')
    for item in lis:
        # print(item)
        save_images(item)
    os.chdir('../')


if __name__ == '__main__':
    pool = Pool()
    groups = ([x for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()
    # for x in range(1, 76):
    #     main(x)
    #     # print(x)
