#!/usr/bin/env python
# encoding: utf-8


"""
@author: william
@contact: 1342247033@qq.com
@site: http://www.xiaolewei.com
@file: mail.py
@time: 22/03/2018 23:18
"""

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from core import config

_smtp = None


def _init():
    global _smtp
    _smtp = smtplib.SMTP_SSL("smtp.qq.com", 465)
    _smtp.login(config.get('app.mail.account'), config.get('app.mail.password'))


def send(receivers, title, content, mime_type='html'):
    global _smtp
    if _smtp is None:
        _init()
    message = MIMEText(content, mime_type, 'utf-8')
    message['From'] = Header('yugong', 'utf-8')
    message['Subject'] = Header(title, 'utf-8')
    _smtp.sendmail(config.get('app.mail.account'), receivers, message.as_string())

