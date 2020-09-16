from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class DefaultPageView(TemplateView):
    template_name = 'rent/base.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
