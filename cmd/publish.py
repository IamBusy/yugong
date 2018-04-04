#!/usr/bin/env python
# encoding: utf-8


"""
@author: william
@contact: 1342247033@qq.com
@site: http://www.xiaolewei.com
@file: publish.py
@time: 07/03/2018 00:45
"""

import sys
import time
import json
from core import db, config, logger
from publisher.toutiao import Toutiao, ToutiaoOperator
from entities import Article


def publish_toutiao():
    client = db.get_redis_client(config.get('app.redis'))
    published_key = 'published_articles'
    publisher = Toutiao()
    logger.info('Start toutiao publish-processing...')
    article_str = client.lpop('fetched_article')
    if isinstance(article_str, bytes):
        article_str = bytes.decode(article_str)
    while article_str and len(article_str) > 0:
        logger.info('Fetched article str from redis')
        try:
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


def operate_toutiao():
    try:
        operator = ToutiaoOperator()
        operator.schedule()
    except Exception as e:
        del operator


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'publish' and sys.argv[2] == '--immediately':
        publish_toutiao()
    elif len(sys.argv) > 1 and sys.argv[1] == 'operate' and sys.argv[2] == '--immediately':
        operate_toutiao()
    else:
        publish_time_point = [6, 17]
        last_publish_time = None
        operate_time_point = [6, 8, 11, 12, 16, 17, 18, 20, 22]
        last_operate_time = None
        while True:
            t = time.localtime(time.time())
            if t.tm_hour in publish_time_point and t.tm_hour != last_publish_time:
                try:
                    logger.info('Start publish')
                    publish_toutiao()
                except Exception as e:
                    logger.info(e)
                finally:
                    last_publish_time = t.tm_hour
            if t.tm_hour in operate_time_point and t.tm_hour != last_operate_time:
                try:
                    logger.info('Start operate')
                    operate_toutiao()
                except Exception as e:
                    logger.info(e)
                finally:
                    last_operate_time = t.tm_hour
            time.sleep(600)


