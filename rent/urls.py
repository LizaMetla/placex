from django.contrib.auth.views import LogoutView
from django.urls import path

from rent.views import *

urlpatterns = [
    path('', DefaultPageView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('advert/add/', AddAdvertView.as_view(), name='advert_add'),
    path('advert/<int:pk>', AdvertDetailView.as_view(), name='advert-detail')
]
