#!/usr/bin/env python
# encoding: utf-8


"""
@author: william
@contact: 1342247033@qq.com
@site: http://www.xiaolewei.com
@file: fetch.py
@time: 07/03/2018 00:09
"""
import json
import time
from fetcher import jianshu
from core import db, config, logger
from analysis.analytizer import Analytizer

if __name__ == '__main__':
    fetchers = [jianshu.Jianshu()]
    analytizer = Analytizer()
    client = db.get_redis_client(config.get('app.redis'))
    time_point = [6, 17]
    while True:
        try:
            t = time.localtime(time.time())
            if t.tm_hour not in time_point:
                continue
            articles = []
            for f in fetchers:
                for article in f.fetch():
                    analytizer.estimate(article)
                    articles.append(article)
            articles = sorted(articles, reverse=True)
            for article in articles:
                article.summary = None
                article_str = json.dumps(article, default=lambda obj: obj.__dict__)
                client.rpush('fetched_article', article_str)
            time.sleep(3600)
        except Exception as e:
            logger.error(e)
        finally:
            time.sleep(600)
