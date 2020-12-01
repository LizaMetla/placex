from django.contrib.auth.views import LogoutView
from django.urls import path

from rent.views import *

urlpatterns = [
    path('', DefaultPageView.as_view(), name='home'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('favorites/', FavoritesView.as_view(), name='favorites'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('advert/add/', AddAdvertView.as_view(), name='advert_add'),
    path('profile/edit/', EditProfileView.as_view(), name='profile_edit'),
    path('advert/<int:pk>', AdvertDetailView.as_view(), name='advert-detail'),
    path('add-to-favorite/<int:pk>/', AddToFavoriteView.as_view(), name='add-to-favorite'),
    path('remove-from-favorite/<int:pk>/', RemoveFromFavoriteView.as_view(), name='remove-to-favorite')
]
