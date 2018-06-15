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


def publish_toutiao(event, context):
    import json
    from publisher.toutiao.publisher import Toutiao
    from core import logger, config, db
    from entities import Article

    client = db.get_redis_client(config.get('app.redis'))
    published_key = 'published_articles'
    publisher = Toutiao()
    logger.info('Start toutiao publish-processing...')
    article_str = client.lpop('fetched_article')
    while article_str and len(article_str) > 0:
        logger.info('Fetched article str from redis')
        try:
            if isinstance(article_str, bytes):
                article_str = bytes.decode(article_str)
            article_json = json.loads(article_str)
            article = Article()
            article.rebuild(article_json)
            title = repr(article.title)
            logger.info('Pre-publish article [%s]' % title)
            if article and (not client.sismember(published_key, title)):
                publisher.publish(article)
                client.sadd(published_key, title)
            else:
                logger.error('Pre-publish article [%s] error, due to published before' % title)
        except Exception as e:
            logger.error('Pickle loads article error')
            logger.error(e)
        finally:
            article_str = client.lpop('fetched_article')


if __name__ == '__main__':
    fetch(None, None)
