from django.urls import path
from . import views

urlpatterns = [
    path('cvSignup', views.cvSignup, name='cvSignup'),
    path('cvSignupVerifyEmail/<str:alt_id>', views.cvSignupVerifyEmail, name='cvSignupVerifyEmail'),
    path('cvSignupConf/<str:alt_id>', views.cvSignupConf, name='cvSignupConf'),
    path('cvSignupCvCreation/<str:alt_id>', views.cvSignupCvCreation, name='cvSignupCvCreation'),
    
    path('companySignup', views.companySignup, name='companySignup'),
    path('companySignupConf/<str:alt_id>', views.companySignupConf, name='companySignupConf'),
    path('companySignupVerifyEmail/<str:alt_id>', views.companySignupVerifyEmail, name='companySignupVerifyEmail'),
    
    path('SignupSetupProcess/<str:alt_id>', views.SignupSetupProcess, name='SignupSetupProcess'),

    path('login', views.Login, name='Login'),
    path('Logout', views.Logout, name='Logout'),

    path('Profile', views.Profile, name='Profile'),
    path('CVProfile', views.CVProfile, name='CVProfile'),
    path('CPProfile', views.CPProfile, name='CompanyProfile'),
    path('CompanySettingGernral', views.CompanySettingGernral, name='CompanySettingGernral'),



    path('Settings', views.Settings, name='Settings'),

    path('CVSettingsGernral', views.CVSettingsGernral, name='CVSettingsGernral'),    
    path('SettingsCV', views.SettingsCV, name='SettingsCV'),

    
]