from django.http import HttpResponse
from django.urls import reverse


def htmx_redirect(path: str, **kwargs) -> HttpResponse:
    response = HttpResponse()
    response["hx-redirect"] = reverse(path, kwargs=kwargs)
    return response
