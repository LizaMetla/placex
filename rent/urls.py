from django.urls import path

from rent.views import *

urlpatterns = [
    path('', DefaultPageView.as_view(), name='default'),
    path('advert/<int:pk>', AdvertDetailView.as_view(), name='advert-detail')
]
