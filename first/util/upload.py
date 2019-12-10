import io
import os
import uuid
from qiniu import Auth, put_file, etag
import qiniu.config
from django.conf import settings

q = qiniu.Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)


def upload(imgName,key):
    token = q.upload_token(settings.QINIU_BUCKET_NAME, key, 3600)
    info = put_file(token, key, imgName)#上传至七牛云
    os.remove(imgName);#文件删除
    tempUrl = settings.QINIU_CALLBACK
    url = tempUrl % key
    print(url)
    return url

