# -*- coding: utf-8 -*-

from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils import simplejson
from django import template
from django.utils.translation import ugettext as _

import re

register = template.Library()

@register.filter(name='category_to_class')
def category_to_class(category):
    
    map_class = {
        'red'   : 'danger',
        'yellow': 'warning',
        'green' : 'success'
    }
    
    try:
        return map_class[category.lower()]
    except:
        return 'default'


@register.filter(name='cm2m')        
def cm2m(value):
    return round(value/100, 2)
    
@register.filter(name='jsonify', is_safe=True)
def jsonify(object):
    if isinstance(object, QuerySet):
        return serialize('json', object)
    return simplejson.dumps(object)

@register.filter(name='every_datetime')  
def every_datetime(value):
    value = ' '.join(re.findall('[A-Z][^A-Z]*', value.encode('utf-8'))[1:])
    if not value:
        value = 'one minute'
    return _('Every %ss' % value.lower())
    
