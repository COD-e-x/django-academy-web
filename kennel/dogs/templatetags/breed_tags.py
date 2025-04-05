from django import template

register = template.Library()


@register.filter
def breeds_media(val):
    if val:
        return f"/media/{val}"
    return "/dogs/images/default-dog.jpg"
