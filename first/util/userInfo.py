import http.client
import urllib.parse
import json
import time

from django.shortcuts import redirect, render
from . import sendUrlRequest
from .. import models
from .. import accessToken
from django.conf import settings
APPID = 'wx7a905758f3506c32'
APPSECRET = '09addc892dc350d1182fe8ee6cd3a2c4'
TOKEN = 'whw'
openid = settings.OPENID
#根据openid获取用户信息
def getUserInfo(setting):
    # openid = 'oEpY-s_OgYNDVChJwwbnVXt1d49A'
    access = accessToken.send_request()
    conn = http.client.HTTPSConnection("api.weixin.qq.com")
    str = '/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN' % (access, openid)
    url = urllib.parse.quote(str, safe=':/?=&')  # 进行url编码
    conn.request("GET", url)
    res = conn.getresponse()
    ac = json.loads(res.read().decode("utf-8"))
    print(ac)
    return ac

#获取网页授权code
def webCode():
    redirt_uri = 'http://whwweixin.free.idcfengye.com/first/getToken/'
    str = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect' % (
    APPID, redirt_uri)
    return  redirect(str)

#获取网页授权accesstoken和信息
from . import jssdk
def getWebToken(request):
    code = request.GET.get('code',None)
    con = 'api.weixin.qq.com'
    str = '/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (APPID,APPSECRET,code)
    res = sendUrlRequest.sedUrl(con,str)
    ac = json.loads(res.read().decode("utf-8"))
    access_token = ac['access_token']
    str2 = '/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN' %(access_token,openid)
    res2 = sendUrlRequest.sedUrl(con, str2)
    ac2 = json.loads(res2.read().decode("utf-8"))
    print(ac2["openid"])
    url = "http://whw.free.idcfengye.com/first/getToken/?code=%s&state=STATE" % code
    context = jssdk.getticket(url)
    print(context)
    context["openid"] = ac["openid"]
    return render(request, 'companyForm.html',context)

# def checkAccessToken(accesstoken,openid):
#     con = 'api.weixin.qq.com'
#     str = 'sns/auth?access_token=%s&openid=%s' %(accesstoken,openid)
#     res1 = sendUrlRequest.sedUrl(con, str)
#     ac = json.loads(res1.read().decode("utf-8"))
#     return ac['errmsg']