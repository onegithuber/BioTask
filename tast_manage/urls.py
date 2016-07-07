# coding=utf-8
"""tast_manage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

import primer_design
from tast import views
from tast import urls
import xadmin
from xadmin.plugins import xversion  # version模块自动注册需要版本控制的 Model

xadmin.autodiscover()

xversion.register_models()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'xadmin/', include(xadmin.site.urls)),
    url(r'', include('tast.urls', namespace='all')),
    url(r'^comments/', include('comments.urls')),
    url(r'^hla/', include('primer_design.urls', namespace='hla')),
]
