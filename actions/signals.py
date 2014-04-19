#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is were we difine the signals to send in response to various actions

"""
# Import python libs
import logging

# Import third party libs
import django.dispatch

# Setup logger
log = logging.getLogger(__name__)


action = django.dispatch.Signal(providing_args=["source", "target", "verb"])
