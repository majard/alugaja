
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def house_is_within_distance(context, house):
    distance = context['distance']
    location = context['location']
    if house.calculate_distance(location) < distance:
        return True
    else:
        return False