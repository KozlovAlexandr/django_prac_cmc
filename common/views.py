from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, ProfileEditForm
from django.contrib.auth.forms import AuthenticationForm


def logout_view(request):

    logout(request)
    return redirect('common:login')


class RegisterView(View):

    def get(self, request):
        return render(request, "common/register.html", {"form": SignUpForm()})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('common:home')

        return render(request, "common/register.html", {'form' : form})


class LoginView(View):

    def get(self, request):
        context = {'form': AuthenticationForm()}
        return render(request, "common/login.html", context)

    def post(self, request):

        authForm = AuthenticationForm(data=request.POST)
        if authForm.is_valid():
            login(request, authForm.get_user())
            return redirect('common:home')
        else:
            context = {'form': authForm}
            return render(request, 'common/login.html', context)


@login_required(login_url=reverse_lazy('common:login'))
def detail_profile(request):

    return render(request, 'common/detail_profile.html', {'profile' : request.user.profile })


@login_required(login_url=reverse_lazy('common:login'))
def profile_edit(request):

    if request.method == 'POST':

        form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('common:detail_profile')
        return render(request, 'common/edit_profile.html', {'form': form})

    if request.method == 'GET':

        form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'common/edit_profile.html', {'form': form})