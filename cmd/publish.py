#!/usr/bin/env python
# encoding: utf-8


"""
@author: william
@contact: 1342247033@qq.com
@site: http://www.xiaolewei.com
@file: publish.py
@time: 07/03/2018 00:45
"""

import time
import json
from core import db, config, logger
from publisher.toutiao import Toutiao
from entities import Article


if __name__ == '__main__':
    client = db.get_redis_client(config.get('app.redis'))
    publish_point = [6, 17]
    publisher = Toutiao()
    published_key = 'published_articles'
    while True:
        try:
            t = time.localtime(time.time())
            if t.tm_hour in publish_point:
                logger.info('At the publish-point [%d], start processing...' % t.tm_hour)
                article_str = client.lpop('fetched_article')
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
                logger.info('Start to sleep... [3600s]')
                time.sleep(3600)
        except Exception as e:
            logger.error(e)
        finally:
            time.sleep(600)

