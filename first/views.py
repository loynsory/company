import base64
import hashlib
import string

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from django.utils.encoding import smart_str
from .util import userInfo as user
from . import accessToken
from .util import sendUrlRequest
from .util import jssdk
from django.conf import settings

# Create your views here.
APPID = 'wx7a905758f3506c32'
APPSECRET = '09addc892dc350d1182fe8ee6cd3a2c4'
TOKEN = 'whw'


@csrf_exempt
def wechat_main(request):
    if request.method == "GET":
        # 接收微信服务器get请求发过来的参数
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        # 服务器配置中的token
        # # 把参数放到list中排序后合成一个字符串，再用sha1加密得到新的字符串与微信发来的signature对比，如果相同就返回echostr给服务器，校验通过
        hashlist = [TOKEN, timestamp, nonce]
        hashlist.sort()
        hashstr = ''.join([s for s in hashlist])
        s1 = hashlib.sha1()
        s1.update(hashstr.encode("utf8"))
        hashstr1 = s1.hexdigest()
        if hashstr1 == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("field")
        # try:
        #     check_signature(TOKEN, signature, timestamp, nonce)
        # except InvalidSignatureException:
        #     return HttpResponse("field")
    else:
        # accessToken.defi_menu()
        othercontent = autoreply(request)
        return HttpResponse(othercontent)


# 审核页面
def userInfo(request):
    redirt_uri = 'http://whw.free.idcfengye.com/first/getToken/'  # 获取网页授权重定向
    str = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect' % (
    APPID, redirt_uri)
    return redirect(str)
    # context = jssdk.getticket("http://whwweixin.free.idcfengye.com/first/userInfo/")
    # print(context)
    # return render(request, 'userInfo.html',context)


# 审核查询页面
def check(request):
    nickname = request.GET.get("nickname")
    print(nickname)
    return render(request, 'success.html')


# 图片上传接口
from .util import upload as up


@csrf_exempt
def upload(request):
    temp = request.POST.get("base64")
    test = request.POST.get("test")
    file = temp.split('base64,')
    image = base64.b64decode(file[1])
    imagename = '%s.%s' % (int(time.time()), "jpg")
    key = int(time.time())
    imagenames = '%s/%s' % (settings.MEDIA_ROOT, imagename)
    fimg = open(imagenames, "wb")
    fimg.write(image)
    fimg.close()

    url = up.upload(imagenames, key)

    data = {'code': '0', 'result': 'success'}
    data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(data)


# 菜单创建
from wechatpy import WeChatClient


def defi_menu(request):
    client = WeChatClient(APPID, APPSECRET, accessToken.send_request())
    client.menu.create({
        "button": [
            {
                "name": "公司注册",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "订单提交",
                        "url": "http://whw.free.idcfengye.com/first/userInfo/"
                    },
                    {
                        "type": "view",
                        "name": "进度查询",
                        "url": "http://whw.free.idcfengye.com/first/check/"
                    },
                    {
                        "type": "click",
                        "name": "赞一下我们",
                        "key": "V1001_GOOD"
                    }
                ]
            }
        ]
    })
    return HttpResponse('创建成功')


# 菜单删除
def delete_menu(request):
    client = WeChatClient(APPID, APPSECRET)
    res = client.menu.delete()
    print(res)
    return HttpResponse('删除成功')


import xml.etree.ElementTree as ET


def autoreply(request):
    try:
        webData = request.body
        xmlData = ET.fromstring(webData)
        msg_type = xmlData.find('MsgType').text
        ToUserName = xmlData.find('ToUserName').text
        FromUserName = xmlData.find('FromUserName').text
        CreateTime = xmlData.find('CreateTime').text
        MsgType = xmlData.find('MsgType').text
        MsgId = xmlData.find('MsgId').text

        print(user.getUserInfo(FromUserName))

        toUser = FromUserName
        fromUser = ToUserName

        if msg_type == 'text':
            content = "伍浩威测试"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()

        elif msg_type == 'image':
            content = "图片已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'voice':
            content = "语音已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'video':
            content = "视频已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'shortvideo':
            content = "小视频已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'location':
            content = "位置已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        else:
            msg_type == 'link'
            content = "链接已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()

    except Exception as Argment:
        return Argment


class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text


import time


class TextMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self.__dict)
