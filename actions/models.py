#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
# Import python libs
import logging

# Import third party libs
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

# Import local libs
from signals import action

# Setup logger
log = logging.getLogger(__name__)


class VerbModelManager(models.Manager):
    """
    """
    def resolve_verb_string(self, verb_string):
        """ Resolve a string to a verb """
        try:
            verb = self.get(name=verb_string)
        except ObjectDoesNotExist as e:
            log.error(
                'Verb string did not resolve properly: {0}'.format(e.message))
            raise e
        else:
            return verb


class VerbModel(models.Model):
    """
    """
    #: The name of the verb
    name = models.CharField(max_length=64, unique=True)
    #: A slug for the name, for url use
    slug = models.SlugField(auto_created=True)
    #: The default visibility. Should be false for backend actions.
    public = models.BooleanField(default=False)
    #: Display string template. Just a string useable by str.format
    display_string_template = models.TextField(
        default='src:{0}, verb:{1}, target{2}')
    #: Content type for the meta data: eg, facebook action id etc.
    meta_data_type = models.ForeignKey(ContentType, null=True)
    #; Model State
    removed = models.BooleanField(default=False)

    #: Reverse relationship for all actions associated with the verb
    actions = generic.GenericRelation('ActionModel')
    #: Custom model manager
    objects = VerbModelManager()




class ActionModelManager(models.Manager):
    """
    """
    def new_action(self, source, target, verb_string):
        verb = VerbModel.objects.resolve_verb_string(verb_string)
        #action = None # TODO stub
        action.send(sender=self, source=source, target=target, verb=verb)



class ActionModel(models.Model):
    """
    """
    #: A verb to signify what the action did.
    verb = models.ForeignKey('VerbModel')
    #: The date and time of the action, defaults to creation time.
    datetime = models.DateTimeField(auto_now=True)

    #: The content type of the target object
    target_type = models.ForeignKey(ContentType, related_name='target_content_type')
    #: The id of the target object
    target_id = models.PositiveIntegerField()
    #: A generic object that the action targeted
    target = generic.GenericForeignKey('target_type',  'target_id')

    #: The content type of the source object
    source_type = models.ForeignKey(ContentType, related_name='source_content_type')
    #: The id of the source object
    source_id = models.PositiveIntegerField()
    #: A generic object that was the actor of the action
    source = generic.GenericForeignKey('source_type', 'source_id')

    #: The id of the meta data model
    action_id = models.CharField(max_length=256, null=True, blank=True)

    #; Model State
    removed = models.BooleanField(default=False)

    #: Custom object manager
    objects = ActionModelManager()

    #@properties
    def display_string(self):
        return 'src:{0}, verb:{1}, target:{2}'.format(self.source, self.verb.name, self.target)
        
        
        
