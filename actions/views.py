#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from django.shortcuts import render_to_response

#Local imports
from models import *


def index(request):
    """
    """
    return render_to_response("actions.html",
        {'request': request, 'title':'Actions',})
