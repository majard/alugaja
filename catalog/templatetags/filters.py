
from django import template

register = template.Library()
        
@register.filter()
def humanize(distance):
    if isinstance(distance, float):
        distance = "{0:.2f}".format(distance)
    return distance
        