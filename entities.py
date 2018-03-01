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

    def get_title(self):
        return self._title

    def get_content(self):
        return self._content

    def get_html(self):
        return self._html



