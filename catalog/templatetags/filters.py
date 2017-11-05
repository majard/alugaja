
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def house_distance(context, house):
    distance = context['distance']
    location = context['location']
    return house.calculate_distance(location)
        