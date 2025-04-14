from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseForbidden


class HtmxRedirectMixin:
    def render_htmx_redirect(self):
        response = HttpResponse()
        response["HX-Redirect"] = self.get_success_url()
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get("HX-Request"):
            return self.render_htmx_redirect()
        return response


class IsOwnerOrAdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not (request.user == obj.owner or request.user.is_staff):
            if request.headers.get("HX-Request"):
                response = render(request, "modals/403.html")
                response["HX-Retarget"] = "#modals-container"
                response["HX-Reswap"] = "innerHTML"
                return response
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
