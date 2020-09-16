from django.urls import path

from rent.views import DefaultPageView

urlpatterns =  [
    path('', DefaultPageView.as_view(), name='default')
]