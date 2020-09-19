from django.forms import ModelForm
from .models import Paste
from django import forms


class PasteEditForm(ModelForm):

    class Meta:
        model = Paste
        fields = ['title', 'text', 'expiration_date']
        widgets = {
            'expiration_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }, format='%Y-%m-%dT%H:%M'),
        }