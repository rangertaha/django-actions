#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
# Import python libs
import logging

# import third party libs
from django.conf import settings
from django import template
from django.template import Library, Node

# Import local libs
from ..models import VerbModel, ActionModel

# Setup logger
log = logging.getLogger(__name__)

# Library
register = template.Library()


@register.tag(name="actions_tag")
def actions_tag(parser, token):
    """
    Sudo-code:
        if {% actions_tag %}
            Use the settings for query limit: ACTIONS_TAG_LIMIT

        if {% actions_tag ### %}
            Use the ### int ACTIONS_TAG_LIMIT with the action tag

    """
    ACTIONS_TAG_LIMIT_DEFAULT = 5
    token_len = len(token.split_contents())
    if token_len == 1:
        # If the tag is alone:  {% actions_tag %}
        # Use the default Value from Settings
        if settings.ACTIONS_TAG_LIMIT and isinstance(settings.ACTIONS_TAG_LIMIT, int):
            actions = ActionModel.objects.filter(active=True)[:settings.ACTIONS_TAG_LIMIT]
            log.info('Using global actions_tag settings...')
        # Else us the value given above
        else:
            log.info('Using default actions_tag settings...')
            actions = ActionModel.objects.filter(active=True)[:ACTIONS_TAG_LIMIT_DEFAULT]
        return ActionNode(actions)

    elif token_len == 2:
        # If the tag has a value:  {% actions_tag 123 %}
        tag_name, value = token.split_contents()
        try:
            # Convert value to Integer and continue
            value = int(value)
            actions = ActionModel.objects.filter(active=True)[:value]
            return ActionNode(actions)

        except:
            # If value is not in Integer raise this
            raise template.TemplateSyntaxError(
                "actions_tag requires an interger,  '{0}' given".format(value))
    else:
        # If there is more then 1 value passed in the tag, raise this
        raise template.TemplateSyntaxError(
            "actions_tag may only have a single interger {0} given".format(len(token_len)))


class ActionNode(template.Node):
    """
    """
    def __init__(self, action):
        self.action = action

    def render(self, context ):
        li, ul, eli, eul  = '<li>', '<ul>', '</li>', '</ul>'
        actions_list = []
        for i in self.action:
            target = '{0}{1}{2}'.format(li, i.target, eli)
            verb = '{0}{1}{2}'.format(li, i.verb.name, eli)
            source = '{0}{1}{2}'.format(li, i.source, eli)
            action_item = '{0}{1}{2}'.format(target, verb, source)
            actions_list.append('{0}{1}{2}{3}{4}'.format(li, ul, action_item, eul, eli))

        return '{0}{1}{2}'.format(ul, ''.join(actions_list), eul)




























