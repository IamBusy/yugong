#!/usr/bin/env python
# encoding: utf-8


"""
@author: william
@contact: 1342247033@qq.com
@site: http://www.xiaolewei.com
@file: heap.py
@time: 02/03/2018 22:44
"""

import heapq
from entities import Article

class TopK:
    def __init__(self, k):
        self.k = k
        self.data = []

    def Push(self, elem: Article):
        topk_small = None
        if len(self.data) < self.k:
            heapq.heappush(self.data, elem)
        else:
            topk_small = self.data[0]
        if topk_small and elem > topk_small:
            heapq.heapreplace(self.data, elem)

    def TopK(self):
        return [x for x in reversed([heapq.heappop(self.data) for x in range(len(self.data))])]