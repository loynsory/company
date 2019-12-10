import hashlib
import http.client
import urllib.parse
import json
import time
from _sha1 import sha1

from django.shortcuts import redirect, render
from . import sendUrlRequest
from .. import models
from .. import accessToken
APPID = 'wx7a905758f3506c32'
def getticket(url):
    context = {}
    timestamp = int(time.time())
    noncestr = 'Wm3WZYTPz0wzccnW'

    coon = 'api.weixin.qq.com'
    str = '/cgi-bin/ticket/getticket?access_token=%s&type=jsapi' %(accessToken.send_request())
    res = sendUrlRequest.sedUrl(coon,str)
    ac = json.loads(res.read().decode("utf-8"))
    print(ac)
    ticket = ac['ticket']
    string = 'jsapi_ticket=%s&noncestr=%s&timestamp=%s&url=%s' %(ticket,noncestr,timestamp,url)

    s1 = hashlib.sha1()
    s1.update(string.encode("utf8"))
    signature = s1.hexdigest()
    # signature = sha1(string)

    context['timestamp'] = timestamp
    context['noncestr'] = noncestr
    context['signature'] = signature
    context['appId'] = APPID
    return context
