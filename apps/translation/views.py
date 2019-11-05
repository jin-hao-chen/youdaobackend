import os
import datetime
from flask import Blueprint
from flask.views import MethodView
from flask import (request, jsonify,
                   send_from_directory)
from apps import settings
from apps.translation import tools

translation_bp = Blueprint('translation', __name__)


def translation_get_langs2chinese():
    ret = {
        'code': settings.CODE_OK,
        'items': [
            {
                'name': '英汉'
            },
            {
                'name': '汉汉'
            },
            {
                'name': '日汉'
            },
            {
                'name': '法汉'
            },
            {
                'name': '韩汉'
            },
            {
                'name': '汉英'
            },
            {
                'name': '汉日'
            },
            {
                'name': '汉法'
            },
            {
                'name': '汉韩'
            }
        ]
    }
    return ret


def translation_get_langs():
    ret = {
        'code': settings.CODE_OK,
        'items': [
            {
                'name': '英文'
            },
            {
                'name': '中文'
            },
            {
                'name': '日文'
            },
            {
                'name': '法文'
            },
            {
                'name': '韩文'
            }
        ]
    }
    return ret


LANG_CODE = {
    '英文': 'en',
    '中文': 'zh-CHS',
    '日文': 'ja',
    '法文': 'fr',
    '韩文': 'ko'
}


# lss
def translation_texts():
    texts = request.form.get('inputvalue')
    src = LANG_CODE[request.form.get('srcLang')]
    dst = LANG_CODE[request.form.get('dstLang')]
    data = tools.translate_texts(texts, src, dst)
    try:
        ret = {
            'code': settings.CODE_OK,
            'item': {
                'translation': data['translation'],
                'tSpeakUrl': data['tSpeakUrl']
            },
        }
    except Exception as e:
        ret = {
            'code': settings.CODE_ERR1
        }
    return ret


class TranslationView(MethodView):

    methods = ['GET', 'POST']

    def get(self):
        if request.args.get('langs2chinese') == 'true':
            return jsonify(translation_get_langs2chinese())
        elif request.args.get('langs') == 'true':
            return jsonify(translation_get_langs())
        return 'Hello, world!'

    def post(self):
        if request.args.get('texts') == 'true':
            return jsonify(translation_texts())


translation_bp.add_url_rule('', view_func=TranslationView.as_view(name='translation_view'), endpoint='translation_view', strict_slashes=True)
