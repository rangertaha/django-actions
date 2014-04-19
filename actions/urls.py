#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from django.conf.urls.defaults import   patterns, include, url
from models import *

urlpatterns = patterns('webapp.actions',

# Actions test view
url(r'$', 'views.index', name='actions'),
)
