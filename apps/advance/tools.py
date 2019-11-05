# -*- coding: utf-8 -*-
import os
import hashlib
import uuid
import time
import json
import requests
from pydub import AudioSegment
from PIL import Image, ImageDraw, ImageFont
from apps import settings


def mp3_to_wav(src, dst):
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format='wav')


def add_text(img, text, loc):
    font = ImageFont.truetype('/Library/Fonts/Arial Unicode.ttf', 30)
    draw = ImageDraw.Draw(img)
    loc = loc.split(',')
    draw.text((int(loc[0]), int(loc[1])), text, (255, 255, 255), font=font)
    return img


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def encrypt(sign):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(sign.encode('utf-8'))
    return hash_algorithm.hexdigest()


def do_request(url, data):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    return requests.post(url, data=data, headers=headers)


def ocr(img_base64, lang):
    salt, curtime = str(uuid.uuid1()), str(int(time.time()))
    post_data = {
        'img': img_base64,
        'detectType': '10012',
        'imageType': '1',
        'langType': lang,
        'docType': 'json',
        'signType': 'v3',
        'curtime': curtime,
        'salt': salt,
        'sign': encrypt(settings.YOUDAO_APP_KEY + truncate(img_base64) + salt + curtime + settings.YOUDAO_APP_SECRET),
        'appKey': settings.YOUDAO_APP_KEY
    }
    ret = {
        'code': settings.CODE_OK
    }
    res = do_request(settings.YOUDAO_OCR_URL, post_data)
    res = json.loads(res.text)
    if res['errorCode'] != "0":
        ret['code'] = settings.CODE_ERR
    data = []
    for region in res['Result']['regions']:
        for line in region['lines']:
            start = line['boundingBox']
            text = line['text']
            data.append({
                'loc': start,
                'text': text
            })
    ret['items'] = data
    return ret


def scan_words(text, src, dst):
    ret = {
        'code': settings.CODE_OK
    }
    data = translate(text, src, dst)
    if data['errorCode'] != "0":
        ret['code'] = settings.CODE_ERR
        return ret
    ret['item'] = data['translation']
    return ret


def translate(text, src, dst):
    curtime = str(int(time.time()))
    salt = str(uuid.uuid1())
    sign = encrypt(settings.YOUDAO_APP_KEY + truncate(text) + salt + curtime + settings.YOUDAO_APP_SECRET)
    post_data = {
        'from': src,
        'to': dst,
        'signType': 'v3',
        'curtime': curtime,
        'salt': salt,
        'sign': sign,
        'q': text,
        'appKey': settings.YOUDAO_APP_KEY
    }
    res = do_request(settings.YOUDAO_TRANSLATE_URL, post_data)
    data = json.loads(res.text)
    return data


def baidu_get_token():
    url = "https://openapi.baidu.com/oauth/2.0/token"
    data = {
        'grant_type': 'client_credentials',
        'client_id': settings.BAIDU_API_KEY,
        'client_secret': settings.BAIDU_API_SECRET
    }
    r = requests.post(url, data=data)
    token = json.loads(r.text).get("access_token")
    return token


def recognize(image_base64):
    token = baidu_get_token()
    url = settings.BAIDU_IMAGE_RECOGNITION + '?access_token=' + token
    data = {
        'image': image_base64,
    }
    data_length = len(json.dumps(data).encode('utf-8'))
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': str(data_length)
    }
    r = requests.post(url, data=data, headers=headers)
    text_json = json.loads(r.text)
    if 'error_code' in text_json.keys():
        return None
    result = []
    for e in text_json['result']:
        result.append({
            'keyword': e['keyword'],
            'score': e['score']
        })
    return result


def voice_recognize(audio, sample_rate, nchannels, lang):
    curtime = str(int(time.time()))
    salt = str(uuid.uuid1())
    post_data = {
        'curtime': curtime,
        'salt': salt,
        'sign': encrypt(settings.YOUDAO_APP_KEY + truncate(audio) + salt + curtime + settings.YOUDAO_APP_SECRET),
        'appKey': settings.YOUDAO_APP_KEY,
        'q': audio,
        'signType': 'v2',
        'langType': lang,
        'rate': str(sample_rate),
        'format': 'wav',
        'channel': nchannels,
        'type': 1
    }
    res = do_request(settings.YOUDAO_ASR_URL, post_data)
    res = json.loads(res.text)
    return res['result'][0] if res['errorCode'] == '0' else None
