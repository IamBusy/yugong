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

if __name__ == '__main__':
    fetchers = [jianshu.Jianshu()]
    analytizer = Analytizer()
    toper = TopK(5)
    for fetcher in fetchers:
        for article in fetcher.fetch():
            analytizer.estimate(article)
            toper.Push(article)

    articles = toper.TopK()
    for article in articles:
        print(article.title)
