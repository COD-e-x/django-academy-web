from django import template

register = template.Library()


@register.filter
def dogs_media(val):
    if val:
        return f"/media/{val}"
    return "/static/images/default/default-dog.jpg"


@register.filter
def shorten_filename(value, length=10):
    """Обрезает название файла до определенной длины, оставляя начало и расширение."""
    if not value:
        return value
    name, ext = value.rsplit(".", 1) if "." in value else (value, "")
    if len(name) > length:
        return f"{name[:length]}...{ext}"
    return value
