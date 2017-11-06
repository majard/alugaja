
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def distance_to(context, house):
    distance = context['distance']
    location = context['location']
    return house.calculate_distance(location)
        