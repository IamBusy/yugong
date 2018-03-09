#!/usr/bin/env python
# encoding: utf-8


"""
@author: william
@contact: 1342247033@qq.com
@site: http://www.xiaolewei.com
@file: fetch.py
@time: 07/03/2018 00:09
"""
import pickle
import json
from fetcher import jianshu
from core import db, config, logger
from analysis.analytizer import Analytizer
from entities import Article


if __name__ == '__main__':
    fetchers = [jianshu.Jianshu()]
    analytizer = Analytizer()
    client = db.get_redis_client(config.get('app.redis'))
    # article = Article('title', 'content', 'html')
    # client.rpush('fetched_article', pickle.dumps(article))

    articles = []
    for f in fetchers:
        for article in f.fetch():
            analytizer.estimate(article)
            articles.append(article)
    articles = sorted(articles, reverse=True)
    for article in articles:
        article.summary = None
        article_str = json.dumps(article, default=lambda obj: obj.__dict__)
        logger.debug(article_str)
        client.rpush('fetched_article', article_str)
