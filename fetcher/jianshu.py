#!/usr/bin/env python
# encoding: utf-8


"""
@author: william
@contact: 1342247033@qq.com
@site: http://www.xiaolewei.com
@file: jianshu.py
@time: 01/03/2018 20:44
"""

import requests
from bs4 import BeautifulSoup
from core import config, logger, db
from entities import Article
import user_agent

headers = {'Connection': 'keep-alive',
           'Cache-Control': 'max-age=0',
           'Accept': 'text/html, */*; q=0.01',
           'X-Requested-With': 'XMLHttpRequest',
           'User-Agent': user_agent.generate_user_agent(),
           'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6'}


class Config(object):
    def __init__(self, cfg: dict):
        self.seminars = cfg['seminars'],
        self.limit = cfg['limit'],
        self.debug = cfg['debug'] if 'debug' in cfg else True


class Jianshu:
    _seminar_url = 'https://www.jianshu.com/c/%s?order_by=added_at&page=%d'
    _jianshu = 'https://www.jianshu.com'
    _cache_seminar_key = 'fetcher-jianshu-seminar-%s-last-time'
    _up_to_last_time = False

    def __init__(self, cfg: Config):
        self._config = cfg
        self._set_manager = db.get_redis_client(config.get('app.redis'))

    def fetch_article_from_url(self, url):
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text)
        article = soup.find('div', class_='article')
        title = article.h1.string
        content = article.find('div', class_='show-content')
        for img in content.find_all('img'):
            if 'data-original-src' in img.attrs:
                img['src'] = 'http:' + img['data-original-src']
        return Article(title, content.get_text(), str(content))

    def fetch_from_seminar(self):
        res = []
        for seminar in self._config.seminars:
            logger.info('Start to fetch articles in seminar [%s]' % seminar)
            set_key = 'last_fetched_article_by_seminar_' + seminar
            last_fetched_articles = self._set_manager.smembers(set_key)
            this_fetched_articles = []
            logger.info('Jianshu last fetched articles: %s' % last_fetched_articles)

            page_num = 1
            repeated = False
            num = 0
            while page_num < 3 and (not repeated):
                resp = requests.get(self._seminar_url % (seminar, page_num), headers=headers)
                page_num += 1
                if resp.status_code / 100 != 2:
                    logger.error('Failed to request [%s] ' % (self._seminar_url % (seminar, page_num - 1)))
                    continue
                # logger.debug('Seminar [%s] content: \n %s' % (seminar, resp.text))
                soup = BeautifulSoup(resp.text)

                ul = soup.find('ul', class_='note-list')

                for li in ul.find_all('li'):
                    try:
                        time_span = li.find('span', class_='time')
                        # write_time = time_span['data-shared-at']
                        if num > self._config.limit:
                            repeated = True
                            break
                        a = li.find('a', class_='title')
                        href = a['href']
                        article = self.fetch_article_from_url(self._jianshu + href)
                        if article:
                            title = repr(article.title)
                            if title in last_fetched_articles:
                                repeated = True
                                break
                            res.append(article)
                            this_fetched_articles.append(title)
                            num += 1
                    except Exception as e:
                        logger.error(e)
                        continue

            # clear last fetched articles
            if not self._config.debug:
                num = len(last_fetched_articles)
                while num > 0:
                    self._set_manager.spop(set_key)
                    num -= 1
                for article in this_fetched_articles:
                    title = repr(article.title)
                    self._set_manager.sadd(set_key, title)
        return res

    def fetch(self):
        return self.fetch_from_seminar()

