#!/usr/bin/env python
# encoding: utf-8


"""
@author: william
@contact: 1342247033@qq.com
@site: http://www.xiaolewei.com
@file: publisher.py
@time: 15/06/2018 13:59
"""
from core import config, logger
from bs4 import BeautifulSoup
from entities import Article
from utils import uploader
from zhon.hanzi import punctuation


class ToutiaoPublisher:
    _url = 'https://mp.toutiao.com/open/new_article_post/'
    _headers = {
        'Content-Type': 'application/x-www-form-urlencoded; UTF-8'
    }

    def __init__(self):
        self._access_token = config.get('app.toutiao.access_token')
        self._client_key = config.get('app.toutiao.client_key')
        pass

    def transformer(self, article: Article):
        '''
        :param article:
        :return:
        purify href of img tag
        '''
        soup = BeautifulSoup(article.html)

        # purify image
        for img in soup.find_all('img'):
            try:
                if 'src' in img.attrs:
                    img['src'] = uploader.upload(img['src'])
            except Exception as e:
                logger.error(e)
                continue

        # remove link
        for a in soup.find_all('a'):
            try:
                if 'href' in a.attrs:
                    del a['href']
            except Exception as e:
                logger.error(e)
                continue

        # control length of title 5-30
        # 一个汉字算一个长度，2个字母算一个长度
        alpha_num = 1
        word_num = 0
        for x in range(len(article.title)):
            if alpha_num / 2 + word_num >= 28:
                article.title = article.title[:x]
            if article.title[x] in punctuation or (u'/u4e00' <= article.title[x] <= u'/u9fa5'):
                word_num += 1
            else:
                alpha_num += 1
        if alpha_num / 2 + word_num < 5:
            article.title = '技术专栏-' + article.title

        # append summarize
        summ = ''
        if article.abstract_str:
            summ = '<h1>内容导读</h1><blockquote><p>%s</p></blockquote>' % str(article.abstract_str)
        article.html = summ + str(soup)

    def publish(self, article):
        try:
            self.transformer(article)
            resp = requests.post('%s?access_token=%s&client_key=%s' % (self._url, self._access_token, self._client_key),
                                 {
                                     'title': article.title,
                                     'content': article.html,
                                     'save': 0
                                 }, headers=self._headers, timeout=20)
            res = json.loads(resp.text)
            if res and 'message' in res and res['message'] == 'success':
                logger.info('Publish article [%s] success' % article.title)
            else:
                logger.error('Publish error:')
                logger.error('response: [%s]' % res['data'])
                logger.error('title: [%s]' % article.title)

        except Exception as e:
            logger.error('Toutiao publish [%s] error' % article.title)
            logger.error(e)
            pass
