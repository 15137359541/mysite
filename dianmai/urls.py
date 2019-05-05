from django.conf.urls import url
from dianmai.models import *
from dianmai.views import *

app_name='dianmai'
urlpatterns=[
    url(r'^$',pic,name='pic'),
    #表单提交
    url(r'^dealStock/$',dealStock,name='dealStock'),
    #证券选择，查看可用余额
    url(r'^securities$',securities,name='securities'),
    url(r'^getPriceNow$',getPriceNow,name='getPriceNow'),



]

#可以加分组
#保证绝对路径   用拼接  {%url 'dept:deptdetail'%}

#正则的分组 （）（）  group（1）拿到第一个分组的信息