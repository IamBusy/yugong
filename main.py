#!/usr/bin/env python
# encoding: utf-8


"""
@author: william
@contact: 1342247033@qq.com
@site: http://www.xiaolewei.com
@file: main.py
@time: 01/03/2018 21:55
"""
from fetcher import jianshu
from analysis.analytizer import Analytizer
from heap import TopK
from publisher.toutiao import Toutiao
from entities import Article
from publisher import dayu

if __name__ == '__main__':
    dy = dayu.Dayu()
