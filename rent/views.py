from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import View

from django.views.generic import TemplateView, DetailView, ListView

from rent.forms import AdvertForm, RegistrationForm, CustomUserCreationForm
from rent.models import Advert

class AbsAuthView(LoginRequiredMixin):
    login_url = reverse_lazy('login')

class DefaultPageView(ListView):
    template_name = 'rent/index.html'
    paginate_by = 20
    context_object_name = 'adverts_list'
    def get_queryset(self):
        return Advert.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['view_name'] = 'home'
        return context


class AdvertDetailView(DetailView):
    template_name = "rent/advert-detail.html"
    model = Advert
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['view_name'] = 'advert_detail'
        return context

class MyAdvertsView(TemplateView):
    template_name = ...
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

class CustomLoginView(LoginView):
    template_name = 'rent/login.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['registration_form'] = CustomUserCreationForm(self.request.POST or None)
        context['view_name'] = 'login'
        return context
class RegisterView(View):
    def post(self, request, *args, **kwargs):
        return redirect('home')
    # def get_context_data(self, **kwargs):

class AddAdvertView(AbsAuthView, TemplateView):
    template_name = 'rent/add-advert.html'
    def get_context_data(self, **kwargs):
        context = super(AddAdvertView, self).get_context_data(**kwargs)
        context['form'] = AdvertForm(self.request.POST or None)
        return context
class RegistrationView(TemplateView):
    template_name = 'rent/login.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registration_form'] = CustomUserCreationForm(self.request.POST or None)
        return context
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if context['registration_form'].is_valid():
            user = context['registration_form'].save()
            login(request, user=user)
        return render(request, self.template_name, context)
