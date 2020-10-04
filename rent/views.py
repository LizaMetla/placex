from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, DetailView, ListView

from rent.models import Advert


class DefaultPageView(ListView):
    template_name = 'rent/index.html'
    paginate_by = 20
    context_object_name = 'adverts_list'
    def get_queryset(self):
        return Advert.objects.all()


class AdvertDetailView(DetailView):
    template_name = "rent/advert-detail.html"
    model = Advert

class MyAdvertsView(TemplateView):
    template_name = ...
    def get(self, request, *args, **kwargs):

        return render(request, self.template_name, {})