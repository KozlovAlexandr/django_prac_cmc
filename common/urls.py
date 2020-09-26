from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name = 'common'
urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('home', views.HomeView.as_view(), name='home'),
    path('logout', views.logout_view, name='logout_view'),
    path('', RedirectView.as_view(url='home')),
]