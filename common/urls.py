from django.urls import path
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
import os

from . import views

app_name = 'common'
urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.logout_view, name='logout'),
    path('profile', views.detail_profile, name='detail_profile'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
    path('profile/pass/change', views.MyPwChangeView.as_view(), name='change_pass'),
    path('profile/pass/reset', views.MyPwResetView.as_view(), name='reset_pass'),
    path('profile/pass/reset/done', views.MyPwResetDoneView.as_view(), name='reset_pass_done'),
    path('profile/pass/reset/confirm/<str:uidb64>/<str:token>', views.MyPwResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('', RedirectView.as_view(url=reverse_lazy('paste:show_all')), name='home'),
]