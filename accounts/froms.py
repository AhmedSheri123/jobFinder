from django import forms
from .models import CompanyProfile, SubscriptionsModel, SubscriptionPriceByCountry, AdminADSModel, CountrysModel, NationalityModel, AdminPermissionModel, HealthStatusModel

class CompanyProfileForm(forms.ModelForm):

    class Meta:
        model = CompanyProfile
        
        fields = ['complite_name', 'company_name', 'about_me', 'country', 'employee_city', 'district', 'img_base64', 'land_line_number' ,'facebook_profile' ,'linkedin' ,'whatsapp' ,'instgram' ,'snapshat' ,'tiktok']
        widgets = {
            'complite_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'about_me': forms.Textarea(attrs={'class': 'form-control mb-3', 'row':6}),
            'country': forms.Select(attrs={'class': 'form-control mb-3'}),
            'employee_city': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'district': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'img_base64':forms.HiddenInput(),
            'land_line_number': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'facebook_profile': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'linkedin': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'instgram': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'snapshat': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'tiktok': forms.TextInput(attrs={'class': 'form-control mb-3'}),

            
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
        fields = ['img', 'redirect_url', 'country', 'available_num_of_days', 'is_main_ad', 'show_in_cv', 'show_in_others', 'show_on_all_countrys', 'is_enabled']


class CountrysModelForm(forms.ModelForm):

    class Meta:
        model = CountrysModel
        fields = ['name']


class NationalityModelForm(forms.ModelForm):

    class Meta:
        model = NationalityModel
        fields = ['name']

class HealthStatusModelForm(forms.ModelForm):

    class Meta:
        model = HealthStatusModel
        fields = ['name']


class AdminPermissionModelForm(forms.ModelForm):

    class Meta:
        model = AdminPermissionModel
        fields = '__all__'