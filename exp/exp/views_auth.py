from django.http import JsonResponse, HttpResponse

import urllib.request
import urllib.parse
import json


def _make_post_request(url, post_data):
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request(url, data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return resp


def _failure(code, error_msg=''):
    if error_msg == '':
        error = { 'status_code' : code }
    else:
        error = { 'status_code' : code, 'error_message' : error_msg }
    return JsonResponse(error)


def login(request, user_type):
    if request.method != 'POST':
        return _failure(400, 'incorrect request type')

    post_data = request.POST.dict()
    post_data['user_type'] = user_type
    url = 'http://models-api:8000/api/auth/login/'
    resp = _make_post_request(url, post_data)

    if resp['status_code'] == 200:
        data = {}
        data['status_code'] = resp['status_code']
        data['auth'] = resp['authenticator']['auth']
        return JsonResponse(data)
    else:
        return _failure(resp['status_code'], resp['error_message'])


def validate(request, user_type):
    if request.method != 'POST':
        return _failure(400, 'incorrect request type')

    post_data = request.POST.dict()
    url = 'http://models-api:8000/api/auth/validate/'
    resp = _make_post_request(url, post_data)

    if resp['status_code'] == 200:
        if user_type == resp['user']['user_type']:
            resp['user'] = resp['user']['info']
            return JsonResponse(resp)
        else:
            return _failure(400, 'incorrect user type')
    else:
        return JsonResponse(resp)


def logout(request):
    if request.method != 'POST':
        return _failure(400, 'incorrect request type')

    post_data = request.POST.dict()
    url = 'http://models-api:8000/api/auth/logout/'
    resp = _make_post_request(url, post_data)
    return JsonResponse(resp)