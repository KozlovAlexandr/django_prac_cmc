from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name = 'compiler'

urlpatterns = [
    path('', views.get_compile_form, name='compile_form'),
    path('api/', views.compile_api, name='compile_api'),
]
