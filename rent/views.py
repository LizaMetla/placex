from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from rent.models import Advert


class DefaultPageView(TemplateView):
    template_name = 'rent/base.html'

    def get(self, request, *args, **kwargs):
        adverts = Advert.objects.all()
        return render(request, self.template_name, {'adverts_list': adverts})
