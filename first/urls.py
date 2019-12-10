from django.urls import path

from . import views
from .util import userInfo as user

urlpatterns = [
    # path('infoPage/', views.infoPage, name='infoPage'),
    path('delete_menu/',views.delete_menu,name = 'delete_menu'),
    path('defi_menu/', views.defi_menu, name='defi_menu'),
    path('', views.wechat_main, name='wechat_main'),
    path('upload/',views.upload,name='uplad'),
    path('getToken/',user.getWebToken,name = 'getToken'),
    path('userInfo/', views.userInfo, name='userInfo'),
    path('check/', views.check, name='check'),
]