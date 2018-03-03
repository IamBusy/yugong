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
from core import config
from entities import Article


class Jianshu:
    _seminar_url = 'https://www.jianshu.com/c/'
    _jianshu = 'https://www.jianshu.com'

    def __init__(self):
        self._seminars = config.get('fetcher.jianshu.seminars')
        self._limit = config.get('fetcher.jianshu.limit')
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
            resp = requests.get(self._seminar_url + seminar)
            if resp.status_code / 100 != 2:
                continue
            soup = BeautifulSoup(resp.text)
            ul = soup.find('ul', class_='note-list')
            num = 0
            for li in ul.find_all('li'):
                try:
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

