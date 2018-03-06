#!/usr/bin/env python
# encoding: utf-8


"""
@author: william
@contact: 1342247033@qq.com
@site: http://www.xiaolewei.com
@file: fetch.py
@time: 07/03/2018 00:09
"""
from fetcher import jianshu
from core import db, config
from analysis.analytizer import Analytizer


if __name__ == '__main__':
    fetchers = [jianshu.Jianshu()]
    analytizer = Analytizer()
    client = db.get_redis_client(config.get('app.redis'))

    articles = []
    for f in fetchers:
        for article in f.fetch():
            analytizer.estimate(article)
            articles.append(article)
    articles = sorted(articles, reverse=True)
    for article in articles:
        client.rpush('fetched_article', article)
