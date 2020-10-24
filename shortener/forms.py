from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import ShortUrl
from django import forms
import datetime


class UrlEditForm(ModelForm):
    class Meta:
        model = ShortUrl
        fields = ['hash', 'expiration_date']
        widgets = {
            'expiration_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }, format='%Y-%m-%dT%H:%M'),
        }


class UrlCreateForm(ModelForm):
    EXP_CHOICES = (('Hour', '1 Hour'), ('Week', '1 Week'), ('Month', '1 Month'), ('Year', '1 Year'))
    EXP_DICT = {'Hour': datetime.timedelta(hours=1), 'Week': datetime.timedelta(weeks=1),
                'Month': datetime.timedelta(days=30), 'Year': datetime.timedelta(days=365)}

    choice_field = forms.ChoiceField(choices=EXP_CHOICES, label="Url expiration", initial='Month')

    def save(self, commit=True):

        if commit:
            return super(UrlCreateForm, self).save(commit=True)

        url = super(UrlCreateForm, self).save(commit=False)

        print(self.cleaned_data['choice_field'])
        url.expiration_date = datetime.datetime.now() + self.EXP_DICT[self.cleaned_data['choice_field']]

        return url

    class Meta:
        model = ShortUrl
        fields = ['original_url']
        widgets = {
            'original_url': forms.URLInput(attrs={
                'formnovalidate': 'formnovalidate',
            }),
        }
