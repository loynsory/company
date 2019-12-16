import http.client
import urllib.parse
import json
import time
from . import models

APPID = 'wx7a905758f3506c32'
APPSECRET = '09addc892dc350d1182fe8ee6cd3a2c4'


def send_request():
    # APPID = 'wx7a905758f3506c32'
    # APPSECRET = '09addc892dc350d1182fe8ee6cd3a2c4'
    access = models.AccessToken.objects.get(id=1)
    if float(access.expiredTime) >= int(time.time()):
        return access.token
    else:
        conn = http.client.HTTPSConnection("api.weixin.qq.com")
        str = '/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (APPID, APPSECRET)
        url = urllib.parse.quote(str, safe=':/?=&')  # 进行url编码
        conn.request("GET", url)
        res = conn.getresponse()
        ac = json.loads(res.read().decode("utf-8"))
        access.token = ac['access_token']
        access.expiredTime = int(time.time()) + float(ac['expires_in'])
        access.save()
        return access.token
