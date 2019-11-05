# -*- coding: utf-8 -*-


import os
import sys
PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJ_DIR)
LIBS_DIR = os.path.join(PROJ_DIR, 'libs')
sys.path.insert(0, LIBS_DIR)
STATIC_DIR = os.path.join(PROJ_DIR, 'static')

API_VERSION = 'v1'
API_PREFIX = '/youdao/api/' + API_VERSION


YOUDAO_OCR_URL = 'https://openapi.youdao.com/ocrapi'
YOUDAO_TRANSLATE_URL = 'https://openapi.youdao.com/api'
YOUDAO_ASR_URL = 'https://openapi.youdao.com/asrapi'
YOUDAO_APP_KEY = 'appkey'
YOUDAO_APP_SECRET = 'appsecret'

BAIDU_IMAGE_RECOGNITION = 'https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general'
BAIDU_API_KEY = 'apikey'
BAIDU_API_SECRET = 'apisecret'


CODE_OK = 0
CODE_ERR = 1
CODE_ERR1 = 2
