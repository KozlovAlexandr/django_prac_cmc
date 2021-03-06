from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    def clean(self):
        super(SignUpForm, self).clean()
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError({"email" : "Email exists"})
        return self.cleaned_data

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ProfileEditForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].required = False

    class Meta:
        model = Profile
        fields = ["website", "about", "avatar"]
