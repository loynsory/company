from django.conf.urls import url
from test_api import views

urlpatterns = [
    url(r'^test/$', views.test),
]

