#!/usr/bin/env python
# encoding: utf-8


"""
@author: william
@contact: 1342247033@qq.com
@site: http://www.xiaolewei.com
@file: uploader.py
@time: 03/03/2018 12:15
"""

import time
from qiniu import Auth, put_file, BucketManager
from core import config, logger
import random

_q = Auth(config.get('app.qiniu.access_key'), config.get('app.qiniu.secret_key'))
_bucket = config.get('app.qiniu.bucket')
_domain = config.get('app.qiniu.domain')
_bucket_manager = BucketManager(_q)


def upload(url: str):
    key = 'yugong/' + str(int(time.time())) + str(random.random()) + '.jpg'
    token = _q.upload_token(_bucket, key, 3600)
    try_time = 3
    while try_time >= 0:
        # fetch resource on network
        if url.startswith('http'):
            ret, info = _bucket_manager.fetch(url, _bucket, key)
        else:
            ret, info = put_file(token, key, url)
        if ret and ret['key'] == key:
            logger.info('Qiniu upload [%s] success' % url)
            return _domain + key
    raise ConnectionError('qiniu service is not available')

