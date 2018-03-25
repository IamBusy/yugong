#!/usr/bin/env python
# encoding: utf-8


"""
@author: william
@contact: 1342247033@qq.com
@site: http://www.xiaolewei.com
@file: browser.py
@time: 14/03/2018 16:46
"""

from selenium import webdriver
# from pyvirtualdisplay import Display
#
# # display = Display(visible=1, size=(800, 600))
# display = Display(visible=1)
# display.start()


def get():
    browser = webdriver.Chrome()
    browser.set_window_size(800, 600)
    return browser
