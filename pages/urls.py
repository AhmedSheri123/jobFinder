from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Subscriptions', views.Subscriptions, name='Subscriptions'),
    path('ContactUs', views.ContactUs, name='ContactUs'),
    path('AdvancedSearch', views.AdvancedSearch, name='AdvancedSearch'),
    path('TermsConditions', views.TermsConditions, name='TermsConditions'),
    path('PrivacyPolicy', views.PrivacyPolicy, name='PrivacyPolicy'),
    path('ContactUs', views.ContactUs, name='ContactUs'),
    path('MostProfit', views.MostProfit, name='MostProfit'),
]