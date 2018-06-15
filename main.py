#!/usr/bin/env python
# encoding: utf-8


"""
@author: william
@contact: 1342247033@qq.com
@site: http://www.xiaolewei.com
@file: main.py
@time: 01/03/2018 21:55
"""


def fetch(event, context):
    # import package
    import json
    from fetcher import jianshu
    from core import config, logger, db

    # init
    cfg = jianshu.Config({
        'seminars': config.get('fetcher.jianshu.seminars'),
        'limit': config.get('fetcher.jianshu.limit'),
        'debug': config.get('app.debug')
    })
    fetchers = [jianshu.Jianshu(cfg)]
    client = db.get_redis_client(config.get('app.redis'))

    articles = []
    for f in fetchers:
        for article in f.fetch():
            articles.append(article)

    articles = sorted(articles, reverse=True)
    for article in articles:
        article.summary = None
        article_str = json.dumps(article, default=lambda obj: obj.__dict__)
        rtn = client.rpush('fetched_article', article_str)
        if rtn:
            logger.info('Push [%s] to redis successfully' % repr(article.title))


if __name__ == '__main__':
    fetch()
