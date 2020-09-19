from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('', views.show_all, name='show_all'),
    path('my/', views.show_my_pastes, name='show_my_pastes'),
    path('<str:paste_hash>/edit/', views.edit, name='edit'),
    path('<str:paste_hash>/', views.detail, name='detail'),
]