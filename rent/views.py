import urllib

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views import View

from django.views.generic import TemplateView, DetailView, ListView

from rent.forms import AdvertForm, CustomUserCreationForm, SearchForm, CustomUserChangeForm
from rent.models import Advert, Image, User


class AbsAuthView(LoginRequiredMixin):
    login_url = reverse_lazy('login')


class DefaultPageView(ListView):
    template_name = 'rent/index.html'
    paginate_by = 50
    context_object_name = 'adverts_list'

    def get_queryset(self):
        query = Q()
        cost_min = self.request.GET.get('cost_min')
        if cost_min and cost_min.isdigit():
            query &= Q(price__gte=cost_min)
        cost_max = self.request.GET.get('cost_max')
        if cost_max and cost_max.isdigit():
            query &= Q(price__lte=cost_max)
        is_owner = self.request.GET.get('is_owner')
        if is_owner and is_owner == 'on':
            query &= ~Q(owner__is_agent=True)
        return Advert.objects.filter(query)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['view_name'] = 'home'
        context['form'] = SearchForm(self.request.POST or None)
        querystring = self.request.GET.copy()
        querystring.pop('page', None)
        context['querystring'] = urllib.parse.urlencode(querystring)
        return context


class AdvertDetailView(DetailView):
    template_name = "rent/advert-detail.html"
    model = Advert

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['view_name'] = 'advert_detail'
        context['advert'].see_counter += 1
        context['advert'].save()
        context['images_list'] = [image.file.url for image in context['advert'].images.all()]
        return context


class MyAdvertsView(TemplateView):
    template_name = ...

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class CustomLoginView(LoginView):
    template_name = 'rent/login.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        register_data = self.request.POST.copy()
        self.request.session.save()
        self.request.session['is_error'] = not context['form'].is_valid()
        self.request.session.save()
        register_data.update({'email': register_data.get('username')})
        context['registration_form'] = CustomUserCreationForm(self.request.POST or None)
        context['view_name'] = 'login'
        return context
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)
        response = super(CustomLoginView, self).post(request, *args, **kwargs)
        if not context['form'].is_valid():
            next = self.request.GET.get('next')
            if next:
                return HttpResponseRedirect(next)
            return redirect('home')
        else:
            return response



class RegisterView(View):
    def post(self, request, *args, **kwargs):
        return redirect('home')
    # def get_context_data(self, **kwargs):


class AddAdvertView(AbsAuthView, TemplateView):
    template_name = 'rent/add-advert.html'

    def get_context_data(self, **kwargs):
        context = super(AddAdvertView, self).get_context_data(**kwargs)
        context['form'] = AdvertForm(self.request.POST or None, self.request.FILES)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if context['form'].is_valid():
            advert = context['form'].save()
            advert.owner = request.user
            advert.is_agent = request.user.is_agent
            advert.save()
            files = request.FILES.getlist('file_field')
            for i, file in enumerate(files):
                image = Image.objects.create(file=file, advert=advert)
                if i == 0:
                    image.is_main = True
                image.save()
            return redirect('advert-detail', advert.pk)
        return render(request, self.template_name, context)


class RegistrationView(TemplateView):
    template_name = 'rent/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_data = self.request.POST.copy()
        if request_data:
            request_data['email'] = request_data.get('username')
        context['registration_form'] = CustomUserCreationForm(request_data or None, self.request.FILES)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if context['registration_form'].is_valid():
            user = context['registration_form'].save()
            login(request, user=user)
            return redirect('home')
        return render(request, self.template_name, context)


class AddToFavoriteView(AbsAuthView, View):
    def get(self, request, *args, **kwargs):
        advert = get_object_or_404(Advert, pk=kwargs.get('pk'))
        self.request.user.favorites.add(advert)
        # self.request.user.favorites.
        next_page = request.GET.get('next')
        if next_page:
            return HttpResponseRedirect(next_page)
        else:
            return redirect('home')

class RemoveFromFavoriteView(AbsAuthView, View):
    def get(self, request, *args, **kwargs):
        advert = get_object_or_404(Advert, pk=kwargs.get('pk'))
        self.request.user.favorites.remove(advert)
        # self.request.user.favorites.
        next_page = request.GET.get('next')
        if next_page:
            return HttpResponseRedirect(next_page)
        else:
            return redirect('home')

class FavoritesView(AbsAuthView, ListView):
    template_name = 'rent/favourites.html'
    paginate_by = 21
    context_object_name = 'adverts_list'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['view_name'] = 'favourites'

        return context
    def get_queryset(self):
        query = Q()
        cost_min = self.request.GET.get('cost_min')
        if cost_min and cost_min.isdigit():
            query &= Q(price__gte=cost_min)
        cost_max = self.request.GET.get('cost_max')
        if cost_max and cost_max.isdigit():
            query &= Q(price__lte=cost_max)
        is_owner = self.request.GET.get('is_owner')
        if is_owner and is_owner == 'on':
            query &= ~Q(owner__is_agent=True) | ~Q(is_agent=True)
        return self.request.user.favorites.filter(query)


class ProfileView(AbsAuthView, ListView):
    template_name = 'rent/profile.html'
    paginate_by = 3
    context_object_name = 'adverts_list'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['view_name'] = 'profile'
        return context
    def get_queryset(self):
        return Advert.objects.filter(owner=self.request.user)

class EditProfileView(AbsAuthView, TemplateView):
    template_name = 'rent/edit-profile.html'
    def post(self, request, *args, **kwargs):
        name = self.request.POST.get('name')
        phone = self.request.POST.get('phone')
        username = self.request.POST.get('username')
        image = self.request.FILES.get('image')
        if User.objects.filter(~Q(username=self.request.user.username),username=username).exists():
            return render(request, self.template_name, context={})
        self.request.user.name = name
        self.request.user.username = username
        self.request.user.email = username
        self.request.user.phone_number = phone
        if image:
            self.request.user.image = image
        self.request.user.save()
        return redirect('profile')

