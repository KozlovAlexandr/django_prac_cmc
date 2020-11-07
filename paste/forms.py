from django.forms import ModelForm
from .models import Paste, PasteCatalog
from django import forms
from django.forms import ValidationError
import datetime

class PasteEditForm(ModelForm):

    def __init__(self, user, *args, **kwargs):

        super(ModelForm, self).__init__(*args, **kwargs)
        choices = PasteCatalog.objects.filter(owner=user)
        cur = self.instance.catalog
        self.fields['catalog'] = forms.ModelChoiceField(queryset=choices, initial=cur,
                                                        required=False, empty_label="No folder")

    class Meta:
        model = Paste
        fields = ['title', 'text', 'expiration_date', 'catalog']
        widgets = {
            'expiration_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
        }, format='%Y-%m-%dT%H:%M'),
        }


class PasteCreateForm(ModelForm):

    EXP_CHOICES =(('Hour', '1 Hour'), ('Week', '1 Week'), ('Month', '1 Month'), ('Year', '1 Year'))
    EXP_DICT = {'Hour': datetime.timedelta(hours=1), 'Week': datetime.timedelta(weeks=1), 'Month' : datetime.timedelta(days=30), 'Year': datetime.timedelta(days=365)}

    choice_field = forms.ChoiceField(choices=EXP_CHOICES, label="Paste expiration", initial='Month')

    def __init__(self, user, *args, **kwargs):

        super(ModelForm, self).__init__(*args, **kwargs)

        if not user.is_authenticated:
            user = None
        choices = PasteCatalog.objects.filter(owner=user)
        cur = self.instance.catalog

        self.fields['catalog'] = forms.ModelChoiceField(queryset=choices, initial=cur,
                                                        required=False, empty_label="No folder")

    def save(self, commit=True):

        if commit:
            return super(PasteCreateForm, self).save(commit=True)

        paste = super(PasteCreateForm, self).save(commit=False)

        paste.expiration_date = datetime.datetime.now() + self.EXP_DICT[self.cleaned_data['choice_field']]

        return paste

    class Meta:

        model = Paste
        fields = ['title', 'syntax', 'text', 'catalog']


class CatalogForm(ModelForm):

    def __init__(self, user, *args, **kwargs):

        super(CatalogForm, self).__init__(*args, **kwargs)
        self.user = user
        for paste in Paste.objects.all():
            if paste.owner == user:
                self.fields[paste.hash] = forms.BooleanField(label=paste.title, required=False, initial=False)

    def clean(self):

        cleaned_data = super(CatalogForm, self).clean()
        # if PasteCatalog.objects.filter(owner=self.user, name=cleaned_data.get('name')):
        #     raise ValidationError('Choose other catalog name')

        for k in cleaned_data:
            if k != 'name' and cleaned_data[k]:
                try:
                    paste = Paste.unexpired_objects.get(name=k)
                except:
                    continue

                if paste.owner != self.user:
                    raise ValidationError("Permission denied")

        return cleaned_data


    def save(self, commit=True):

        catalog = super(CatalogForm, self).save(commit=False)
        catalog.owner = self.user
        catalog.save()

        for k in self.fields:
            if k != 'name' and self.cleaned_data[k]:

                paste = Paste.objects.get(hash=k)

                paste.catalog = catalog
                paste.save()

    class Meta:
        model = PasteCatalog
        fields = ['name']



