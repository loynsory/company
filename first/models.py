from django.db import models


# Create your models here.
class AccessToken(models.Model):
    token = models.CharField(max_length=512)
    expiredTime = models.CharField(max_length=30)

    def __str__(self):
        return self.expiredTime


class UserInfo(models.Model):
    openid = models.CharField(max_length=512)
    nickname = models.CharField(max_length=512)
    sex = models.CharField(max_length=5)
    country = models.CharField(max_length=30)
    province = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    access_token = models.CharField(max_length=512)
    expiredTime = models.CharField(max_length=30)


class CheckInfo(models.Model):
    openid = models.CharField(max_length=512)
    name = models.CharField(max_length=30)
    cartId = models.CharField(max_length=30)
    range = models.CharField(max_length=512)
    persent = models.CharField(max_length=512)
    images = models.CharField(max_length=1024)
