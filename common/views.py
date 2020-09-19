from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect

from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm


class HomeView(View):

    def get(self, request):

        if request.user.is_authenticated:
            return render(request, "common/home.html", {'user': request.user})

        else:
            return redirect('login')


def logout_view(request):

    logout(request)
    return redirect('login')


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
            return redirect('home')

        return render(request, "common/register.html", {'form' : form})


class LoginView(View):

    def get(self, request):
        context = {'form': AuthenticationForm()}
        return render(request, "common/login.html", context)

    def post(self, request):

        authForm = AuthenticationForm(data=request.POST)
        if authForm.is_valid():
            login(request, authForm.get_user())
            return redirect('home')
        else:
            context = {'form': authForm}
            return render(request, 'common/login.html', context)