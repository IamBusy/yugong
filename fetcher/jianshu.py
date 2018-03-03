#!/usr/bin/env python
# encoding: utf-8


"""
@author: william
@contact: 1342247033@qq.com
@site: http://www.xiaolewei.com
@file: jianshu.py
@time: 01/03/2018 20:44
"""

import time
import requests
from bs4 import BeautifulSoup
from core import config, cache, logger
from entities import Article


class Jianshu:
    _seminar_url = 'https://www.jianshu.com/c/'
    _jianshu = 'https://www.jianshu.com'
    _cache_seminar_key = 'fetcher-jianshu-seminar-%s-last-time'
    _up_to_last_time = False

    def __init__(self):
        self._seminars = config.get('fetcher.jianshu.seminars')
        self._limit = config.get('fetcher.jianshu.limit')
        self._up_to_last_time = config.get('fetcher.jianshu.up_to_last_time')
        pass

    def fetch_article_from_url(self, url):
        resp = requests.get(url)
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
        for seminar in self._seminars:

            last_fetch_time = cache.get(self._cache_seminar_key % seminar)
            if not last_fetch_time:
                last_fetch_time = 0
            logger.info('Jianshu last fetch [%s] time: %s' % (seminar, last_fetch_time))
            if config.get('app.debug'):
                cache.put(self._cache_seminar_key % seminar, time.time())

            resp = requests.get(self._seminar_url + seminar)
            if resp.status_code / 100 != 2:
                continue
            soup = BeautifulSoup(resp.text)

            ul = soup.find('ul', class_='note-list')
            num = 0

            for li in ul.find_all('li'):
                try:
                    # Judge shared time to avoid repeated fetching
                    time_span = li.find('span', class_='time')
                    shared_time = time_span['data-shared-at']
                    if self._up_to_last_time and time.mktime(time.strptime(shared_time, '%Y-%m-%dT%H:%M:%S+08:00')) <= last_fetch_time:
                        logger.info('Jianshu fetch article(time:%s) up to last time(%s)' % (shared_time, last_fetch_time))
                        break
                    if num > self._limit:
                        break
                    a = li.find('a', class_='title')
                    href = a['href']
                    article = self.fetch_article_from_url(self._jianshu + href)
                    if article:
                        res.append(article)
                        num += 1
                except Exception as e:
                    continue
        return res

    def fetch(self):
        return self.fetch_from_seminar()

