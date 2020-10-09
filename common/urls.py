from django.urls import path
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy

from . import views

app_name = 'common'
urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.logout_view, name='logout'),
    path('profile', views.detail_profile, name='detail_profile'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
    path('', RedirectView.as_view(url=reverse_lazy('paste:show_all'))),
]