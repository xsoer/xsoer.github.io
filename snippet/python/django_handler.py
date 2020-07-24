import logging
import requests
import traceback
from django.http import JsonResponse
import time
from django.conf import settings
import json


def handler_rsp(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        rsp = {'code': 0, 'msg': 'ok', 'data': None}
        try:
            result = func(*args, **kwargs)
            rsp.update(result)
        except Exception:
            err = traceback.format_exc()
            logging.error(err)
            call_dingding(err)
            rsp.update({'code': -1, 'msg': '后端服务异常，请稍后重试！', 'data': None})
        return JsonResponse(rsp)
    return wrapper


def call_dingding(content, mobiles=['18210275388']):
    msg = f"项目:{settings.CONF['project']},环境:{settings.CONF['env']}\n{content}"
    try:
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = {
            "msgtype": "text",
            "text": {
                "content": msg
            },
            "at": {
                "atMobiles": mobiles,
                "isAtAll": False
            }
        }
        url = 'https://oapi.dingtalk.com/robot/send?access_token=039cb5d1843ff2668b7d3685b20a0b9b11df2257304d2f2c477a2291f36a74c2'
        requests.post(url=url, headers=headers, data=json.dumps(data))
    except Exception as e:
        print(str(e))
