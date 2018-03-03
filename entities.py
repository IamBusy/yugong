#!/usr/bin/env python
# encoding: utf-8


"""
@author: william
@contact: 1342247033@qq.com
@site: http://www.xiaolewei.com
@file: entities.py
@time: 01/03/2018 21:41
"""


class Article:
    def __init__(self, title, content, html, **kwargs):
        self._title = title
        self._content = content
        self._html = html
        self._score = 0
        self._summarize = ''

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def content(self):
        return self._content

    @property
    def html(self):
        return self._html

    @html.setter
    def html(self, html):
        self._html = html

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score

    @property
    def summarize(self):
        return self._summarize

    @summarize.setter
    def summarize(self, summarize):
        self._summarize = summarize

    def __cmp__(self, other):
        if self.__eq__(other):
            return 0
        elif self.__lt__(other):
            return -1
        elif self.__gt__(other):
            return 1

    def __eq__(self, other):
        if not isinstance(other, Article):
            raise TypeError("can't cmp other type to Article!")
        return self.score == other.score

    def __lt__(self, other):
        if not isinstance(other, Article):
            raise TypeError("can't cmp other type to Article!")
        return self.score < other.score

    def __gt__(self, other):
        if not isinstance(other, Article):
            raise TypeError("can't cmp other type to Article!")
        return self.score > other.score



