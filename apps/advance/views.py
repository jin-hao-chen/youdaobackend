import os
import time
import uuid
import json
import datetime
import io
import shutil
import base64
import hashlib
from pydub import AudioSegment
import wave
from PIL import Image, ImageDraw, ImageFont
from flask import Blueprint
from flask.views import MethodView
from flask import (request, jsonify,
                   send_from_directory)
import requests
from apps import settings
from apps.advance import tools


advance_bp = Blueprint('advance', __name__)


LANG_CODE = {
    '英汉': ['en', 'zh-CHS'],
    '汉汉': ['zh-CHS', 'zh-CHS'],
    '日汉': ['ja', 'zh-CHS'],
    '法汉': ['fr', 'zh-CHS'],
    '韩汉': ['ko', 'zh-CHS'],
    '汉英': ['zh-CHS', 'en'],
    '汉日': ['zh-CHS', 'ja'],
    '汉法': ['zh-CHS', 'fr'],
    '汉韩': ['zh-CHS', 'ko']
}


def advance_scan_words():
    ret = {
        'code': settings.CODE_OK
    }

    img = request.files.get('image')
    out = img.read()
    img_base64 = base64.b64encode(out).decode('utf-8')

    image = Image.open(io.BytesIO(out))
    data = tools.ocr(img_base64, LANG_CODE[request.form.get('lang')][0])
    if data['code'] == settings.CODE_ERR:
        ret['code'] = settings.CODE_ERR
        return ret

    for line in data['items']:
        data1 = tools.scan_words(line['text'],
                                    LANG_CODE[request.form.get('lang')][0],
                                    LANG_CODE[request.form.get('lang')][1])
        if data1['code'] == settings.CODE_ERR:
            ret['code'] = settings.CODE_ERR
            return ret
        translation = data1['item']
        tools.add_text(image, translation[0], line['loc'])
    byteIO = io.BytesIO()
    image.save(byteIO, format='jpeg')
    item = base64.b64encode(byteIO.getvalue()).decode('utf-8')
    ret['item'] = item
    return ret


def advance_image_recognize():
    ret = {
        'code': settings.CODE_OK
    }
    img = request.files.get('file')
    out = img.read()
    img_base64 = base64.b64encode(out).decode('utf-8')
    result = tools.recognize(img_base64)
    if result is None:
        ret['code'] = settings.CODE_ERR
        return ret
    data = []
    for res in result:
        if res['score'] > 0.3:
            tmp = tools.scan_words(res['keyword'],
                             LANG_CODE[request.form.get('lang')][0],
                             LANG_CODE[request.form.get('lang')][1])
            if tmp['code'] == settings.CODE_ERR:
                ret['code'] = settings.CODE_ERR
                return ret
            data.append(tmp['item'])
    ret['items'] = data
    return ret


def advace_voice_translate():
    audio = request.files['file']
    prefix = audio.filename.split('.')[0]
    old_path = os.path.join(settings.STATIC_DIR, audio.filename)
    audio.save(old_path)

    new_path = os.path.join(settings.STATIC_DIR, prefix + '.wav')
    tools.mp3_to_wav(old_path, new_path)

    os.remove(old_path)
    wav_info = wave.open(new_path, 'rb')
    sample_rate = wav_info.getframerate()
    nchannels = wav_info.getnchannels()
    wav_info.close()

    with open(new_path, 'rb') as file_wav:
        audio_base64 = base64.b64encode(file_wav.read()).decode('utf-8')
    origin = tools.voice_recognize(audio_base64, 16000, nchannels, LANG_CODE[request.form.get('lang')][0])
    if origin is None:
        os.remove(new_path)
        return {
            'code': settings.CODE_ERR
        }
    result = tools.scan_words(origin, LANG_CODE[request.form.get('lang')][0], LANG_CODE[request.form.get('lang')][1])['item'][0]
    ret = {
        'code': settings.CODE_OK,
        'origin': origin,
        'result': result
    }
    os.remove(new_path)
    return ret


# used by search_word()
def _fetch_data(data, name):
    if name in data.keys():
        return data[name]
    return []


# used by search_word()
def _fetch_data2(data, name1, name2):
    ret = _fetch_data(data, name1)
    if ret:
        if name2 in ret.keys():
            return ret[name2]
    return ret


def search_word():
    ret = {
        'code': settings.CODE_OK
    }
    explain = tools.translate(request.form.get('word'),
                           LANG_CODE[request.form.get('lang')][0],
                           LANG_CODE[request.form.get('lang')][1])
    result = {
        'explain': _fetch_data2(explain, 'basic', 'explains'),
        'wfs': _fetch_data2(explain, 'basic', 'wfs'),
        'web': _fetch_data(explain, 'web'),
        'phonetic': _fetch_data2(explain, 'basic', 'phonetic'),
        'translation': _fetch_data(explain, 'translation')[0],
        'speakUrl': _fetch_data(explain, 'speakUrl')
    }
    ret['item'] = result
    return ret


class AdvanceView(MethodView):

    methods = ['GET', 'POST']

    def post(self):
        if request.args.get('scan_words') == 'true':
            return jsonify(advance_scan_words())
        if request.args.get('image_recognition') == 'true':
            return jsonify(advance_image_recognize())
        if request.args.get('voice_translate') == 'true':
            return jsonify(advace_voice_translate())
        if request.args.get('search_word') == 'true':
            return jsonify(search_word())


advance_bp.add_url_rule('', view_func=AdvanceView.as_view(name='advance_view'), endpoint='advance_view', strict_slashes=True)
