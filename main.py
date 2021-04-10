# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
import json
import time
from crawsql import Crawler
import random

import jieba
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud

URL = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100008959687&score=0&sortType=5&page=%s&pageSize=10&isShadowSku=0&fold=1'
kv = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}


def spider_jd(page=0, crawdb=None):
    time.sleep(0.1 * random.randint(0, 9))
    url = URL % page
    r = requests.get(url, headers=kv)
    try:
        r.raise_for_status()
        r = requests.get(url, headers=kv)
        r_json_str = json.loads(r.text[20:-2])
        maxPage = r_json_str.get('maxPage')
    except:
        print('crawler error!')

    if (page < maxPage):

        for item in r_json_str.get('comments'):
            if item is not None:
                content = item.get('content')
                score = item.get('score')
                creatime = item.get('creationTime')
                name = item.get('referenceName')
                u_name = item.get('nickname')
                realtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                u_image = item.get('userImageUrl')
                images = item.get('images')
                videos = item.get('videos')
                if (images and images[0]):
                    image = images[0].get('imgUrl')
                else:
                    image = None
                if (videos and videos[0]):
                    video = videos[0].get('remark')
                else:
                    video = None

                insert_sony(crawdb, content, score, creatime, name, u_name, realtime, u_image, image, video)

        page += 1
        spider_jd(page, crawdb)


def insert_sony(craww, sc_comment, sc_score, sc_creatime, sc_name, u_name, sc_time, u_image, sc_image, sc_video):
    sql = "INSERT INTO sonycomment(sc_comment, sc_score, sc_creatime, sc_name, u_name, sc_time, u_image, sc_image, sc_video) VALUES ('%s',%d,'%s','%s','%s','%s','%s','%s','%s')" % (
        sc_comment, sc_score, sc_creatime, sc_name, u_name, sc_time, u_image, sc_image, sc_video)
    craww.insert_sql(sql)


def data_clear(comments):
    wl = jieba.lcut(comments)
    wl = " ".join(wl)
    return wl


def create_word_cloud(words):
    coloring = np.array(Image.open('sony.jpg'))
    wc = WordCloud(background_color="white", max_words=200, mask=coloring, scale=4, max_font_size=50, random_state=42)

    wc.generate(words)

    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.figure()
    plt.show()


if __name__ == '__main__':
    craww = Crawler('localhost', 'crawler', 'crawler123', 'jd')
    # spider_jd(crawdb=craww)
    sql = 'SELECT sc_comment FROM sonycomment'
    results = craww.query_sql(sql)
    comments = ""
    for res in results:
        comments += res[0]

    create_word_cloud(data_clear(comments))
