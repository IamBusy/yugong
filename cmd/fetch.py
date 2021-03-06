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
    time_point = [6, 17]
    while True:
        try:
            t = time.localtime(time.time())
            if t.tm_hour not in time_point:
                continue
            cfg = jianshu.Config({
                'seminars': config.get('fetcher.jianshu.seminars'),
                'limit': config.get('fetcher.jianshu.limit'),
                'debug': config.get('app.debug')
            })
            fetchers = [jianshu.Jianshu(cfg)]
            analytizer = Analytizer()
            client = db.get_redis_client(config.get('app.redis'))

            articles = []
            for f in fetchers:
                for article in f.fetch():
                    analytizer.estimate(article)
                    articles.append(article)
                del f
            del analytizer
            articles = sorted(articles, reverse=True)
            for article in articles:
                article.summary = None
                article_str = json.dumps(article, default=lambda obj: obj.__dict__)
                rtn = client.rpush('fetched_article', article_str)
                if rtn:
                    logger.info('Push [%s] to redis successfully' % repr(article.title))
            del articles
            logger.info('Starting sleep 3600s...')
            time.sleep(3600)
        except Exception as e:
            logger.error(e)
        finally:
            time.sleep(600)
