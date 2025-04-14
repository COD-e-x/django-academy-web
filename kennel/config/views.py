from django.http import HttpResponse


def clear_modal(request):
    """Закрывает модальное окно (HTMX)"""
    return HttpResponse("")
