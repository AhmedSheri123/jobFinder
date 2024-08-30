from django import forms
from .models import CompanyProfile, SubscriptionsModel, SubscriptionPriceByCountry, AdminADSModel

class CompanyProfileForm(forms.ModelForm):

    class Meta:
        model = CompanyProfile
        
        fields = ['company_name', 'complite_name', 'phone', 'about_me', 'country', 'employee_city', 'district', 'img_base64']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'complite_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'about_me': forms.Textarea(attrs={'class': 'form-control', 'row':6}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'employee_city': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'img_base64':forms.HiddenInput(),
            
        }


class SubscriptionModelForm(forms.ModelForm):

    class Meta:
        model = SubscriptionsModel
        
        fields = '__all__'

        widgets = {
            'creation_date':forms.DateTimeInput(attrs={'type':'datetime-local'})
        }


class SubscriptionPriceByCountryModelForm(forms.ModelForm):

    class Meta:
        model = SubscriptionPriceByCountry
        fields = ['subscription', 'country', 'price', 'currency']


class AdminADSModelForm(forms.ModelForm):

    class Meta:
        model = AdminADSModel
        fields = ['img', 'redirect_url', 'country', 'available_num_of_days', 'is_enabled']