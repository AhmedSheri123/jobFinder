from django import forms
from .models import GeneralSettingsModel


class GeneralSettingsModelForm(forms.ModelForm):
    class Meta:
        model = GeneralSettingsModel
        fields = '__all__'
        # widgets = {
        #     'img':forms.FileInput(attrs={'style':'display:block;'})
        # }