from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.conf import settings
import logging
from django.urls import resolve
from django.core.cache import cache
from django.middleware.csrf import get_token

class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        match = resolve(request.path_info)
        url_name = match.url_name
        # 排除不需要登陆的接口
        if url_name in settings.NO_AUTH_URL:
            return
        # 判断用户是否登陆
        token = request.META.get('HTTP_X_TOKEN', '')
        if token and cache.get(f'access_token:{token}'):
            return
        # 没有token或者token过期，直接让其自动登录。
        return JsonResponse({'code': 403, 'msg': '没有登录，请重新登录！', 'data': None})

    def process_response(self, request, response):
        return response
