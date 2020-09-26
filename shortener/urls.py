from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name = 'shortener'
urlpatterns = [
    path('my/', views.show_my_urls, name='show'),
    path('create/', views.CreateView.as_view(), name='create'),
    # path('<str:url_hash>/edit/', views.edit, name='edit'),
    path('edit/<str:url_hash>/', views.edit, name='edit'),
    path('<str:url_hash>/', views.my_redirect, name='my_redirect'),
]