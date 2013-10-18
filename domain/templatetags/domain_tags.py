
from django import template

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