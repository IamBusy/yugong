#!/usr/bin/env python
# encoding: utf-8


"""
@author: william
@contact: 1342247033@qq.com
@site: http://www.xiaolewei.com
@file: analytizer.py
@time: 01/03/2018 22:02
"""

from entities import Article
from filter import baidu_repetition_rate
from summarizer import summarize
from core import logger

class Analytizer:

    def __init__(self):
        pass

    def estimate(self, article: Article):
        try:
            article.summary = summarize(article)
            for sen in article.summary:
                article.abstract_str += str(sen)
            article.score = baidu_repetition_rate(article)
        except Exception as e:
            logger.error('Estimate article error: [%s]' % article.title)
