from django.forms import ModelForm
from .models import Paste, PasteCatalog
from django import forms
from django.forms import ValidationError


class PasteEditForm(ModelForm):

    def __init__(self, user, *args, **kwargs):

        super(ModelForm, self).__init__(*args, **kwargs)
        choices = PasteCatalog.objects.filter(owner=user)
        cur = self.save(commit=False).catalog
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

    def __init__(self, user, *args, **kwargs):

        super(ModelForm, self).__init__(*args, **kwargs)

        if not user.is_authenticated:
            user = None
        choices = PasteCatalog.objects.filter(owner=user)
        cur = self.save(commit=False).catalog
        self.fields['catalog'] = forms.ModelChoiceField(queryset=choices, initial=cur,
                                                        required=False, empty_label="No folder")

    class Meta:
        model = Paste
        fields = ['title', 'syntax', 'expiration_date', 'text', 'catalog']
        widgets =  {
            'expiration_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }, format='%Y-%m-%dT%H:%M'),
        }


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


    def save(self, commit=True):

        catalog = super(CatalogForm, self).save(commit=False)
        catalog.owner = self.user
        catalog.save()

        for k in self.fields:
            if k != 'name' and self.fields[k]:

                paste = Paste.objects.get(hash=k)

                paste.catalog = catalog
                paste.save()

    class Meta:
        model = PasteCatalog
        fields = ['name']



