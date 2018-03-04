#!/usr/bin/env python
# encoding: utf-8


"""
@author: william
@contact: 1342247033@qq.com
@site: http://www.xiaolewei.com
@file: filter.py
@time: 01/03/2018 22:05
"""

import requests
from bs4 import BeautifulSoup
from entities import Article
from core import logger


def baidu_repetition_rate(article: Article):
    try:
        sentences = article.summary
        totalScore = 0
        sen_num = 0
        for sen in sentences:
            try:
                search_key = str(sen)
                page = search_baidu(search_key)
                soup = BeautifulSoup(page)
                score = 0
                num = 0
                for item in soup.find_all('div', class_='c-container'):
                    try:
                        score += rank_item(article, search_key, item)
                        num += 1
                    except Exception as e:
                        logger.info(e)
                        continue
                if num > 0:
                    sen_num += 1
                    totalScore += score / num
            except Exception as e:
                logger.error(e)
                continue
        finial_score = totalScore / sen_num
        logger.debug('================================')
        logger.debug("[%s]得分：%f" % (article.title, finial_score))
        return finial_score
    except Exception as e:
        logger.error('[%s]摘要错误' % article.title)
        logger.error(e)
        return 0


def search_baidu(key):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}
    resp = requests.get('https://www.baidu.com/s?wd=' + key, headers=headers, timeout=3)
    if resp.status_code / 100 != 2:
        raise Exception('Network error when visiting baidu')
    return resp.content


def rank_item(article: Article, search_key, item):
    # title_score : content_score = 0.3 : 1
    title_conten_rate = 0.3
    title = item.h3.a.get_text()
    # TODO calculate similarity of title
    comm_len = lcs(title, article.title)
    title_score = 1 - (float(comm_len) / len(title)) ** 2

    abstract = item.find('div', class_='c-abstract')
    existed = []
    totalLen = 0
    for child in abstract.contents:
        if child.name == 'span':
            continue
        elif child.name == 'em':
            existed.append(len(child.string))
            totalLen += len(child.string)
        else:
            totalLen += len(child)
    abstract_score = 0
    rate = float(1) / totalLen / totalLen
    for sep_len in existed:
        abstract_score += rate * sep_len * sep_len

    return abstract_score * (1 - title_conten_rate) + title_score * title_conten_rate


def lcs(a, b):
    lena = len(a)
    lenb = len(b)
    c = [[0 for i in range(lenb + 1)] for j in range(lena + 1)]
    for i in range(lena):
        for j in range(lenb):
            if a[i] == b[j]:
                c[i + 1][j + 1] = c[i][j] + 1
            elif c[i + 1][j] > c[i][j + 1]:
                c[i + 1][j + 1] = c[i + 1][j]
            else:
                c[i + 1][j + 1] = c[i][j + 1]
    return c[lena][lenb]
