#!/usr/bin/env python
# encoding: utf-8
from django.conf.urls import url

import views

urlpatterns = [
    url(r'primerdesign', views.PrimerView.as_view(), name='primer'),
    # url(r'primerdown', 'primer_design.views.file_download', name='down'),
    url(r'primerdown/(.+)/', 'primer_design.views.send_zipfile', name='down'),
    url(r'success', 'primer_design.views.successview', name='success'),
]
