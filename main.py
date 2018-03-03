#!/usr/bin/env python
# encoding: utf-8


"""
@author: william
@contact: 1342247033@qq.com
@site: http://www.xiaolewei.com
@file: main.py
@time: 01/03/2018 21:55
"""
from fetcher import jianshu
from analysis.analytizer import Analytizer
from heap import TopK
from publisher.toutiao import Toutiao
from entities import Article

if __name__ == '__main__':
    fetchers = [jianshu.Jianshu()]
    analytizer = Analytizer()
    toper = TopK(5)
    publisher = Toutiao()
    #publisher.publish(Article("this is a title", "", "<h1>标题1</h1><code>$a=1;</code><img href=\"https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1520073375553&di=234a4dd7d2ad4922b8c248d29157800f&imgtype=0&src=http%3A%2F%2Fwww.grabsun.com%2Fuploads%2Fimages%2F2015%2F12%2FwKioL1SYxp2BaBIOAAAhQIoTPTk588.jpg\"/>"))

    for fetcher in fetchers:
        for article in fetcher.fetch():
            analytizer.estimate(article)
            toper.Push(article)

    articles = toper.TopK()
    for article in articles:
        publisher.publish(article)
        print(article.title)
