
from django import template

register = template.Library()
        
@register.filter()
def humanize(distance):
    dist = "{0:.2f}".format(distance)
    return dist
        