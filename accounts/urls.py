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
    path('SendWhaCodeVerify/<str:alt_id>', views.SendWhaCodeVerify, name='SendWhaCodeVerify'),
    path('EmployeeSendWhaCodeVerify/<str:alt_id>', views.EmployeeSendWhaCodeVerify, name='EmployeeSendWhaCodeVerify'),
     
    path('SignupSetupProcess/<str:alt_id>', views.SignupSetupProcess, name='SignupSetupProcess'),
    path('sendEmailCode/<str:alt_id>', views.sendEmailCode, name='sendEmailCode'),
    path('EmployeeSendEmailCodeVerify/<str:alt_id>', views.EmployeeSendEmailCodeVerify, name='EmployeeSendEmailCodeVerify'),
    path('CompanySendEmailCodeVerify/<str:alt_id>', views.CompanySendEmailCodeVerify, name='CompanySendEmailCodeVerify'),

    

    path('login', views.Login, name='Login'),
    path('Logout', views.Logout, name='Logout'),

    path('UserLike/<int:liked_id>', views.UserLike, name='UserLike'),
    path('Profile/<int:id>', views.Profile, name='Profile'),
    path('CVProfile/<int:id>', views.CVProfile, name='CVProfile'),
    path('CPProfile/<int:id>', views.CPProfile, name='CompanyProfile'),
    path('CompanySettingGernral', views.CompanySettingGernral, name='CompanySettingGernral'),



    path('Settings', views.Settings, name='Settings'),
    path('CVSettingsGernral', views.CVSettingsGernral, name='CVSettingsGernral'),    
    path('SettingsCV', views.SettingsCV, name='SettingsCV'),

    path('MyReferralLink', views.MyReferralLink, name='MyReferralLink'),
    path('CreateReferralLinkForMe', views.CreateReferralLinkForMe, name='CreateReferralLinkForMe'),
    path('DeleteReferralLinkForMe/<str:referral_id>', views.DeleteReferralLinkForMe, name='DeleteReferralLinkForMe'),
    path('WithdrawReferralLinkBalance/<str:referral_id>', views.WithdrawReferralLinkBalance, name='WithdrawReferralLinkBalance'),
    path('ref/<str:referral_id>', views.SignUpReferralLink, name='SignUpReferralLink'),
    
    #Subscriptions
    path('EnableUserSubscription/<int:id>', views.EnableUserSubscription, name='EnableUserSubscription'),
    path('DisableUserSubscription', views.DisableUserSubscription, name='DisableUserSubscription'),

    path('CompanyUserSubscription', views.CompanyUserSubscription, name='CompanyUserSubscription'),
    path('EmployeeUserSubscription', views.EmployeeUserSubscription, name='EmployeeUserSubscription'),

    path('CompanyNotificationsSettings', views.CompanyNotificationsSettings, name='CompanyNotificationsSettings'),
    path('EmployeeNotificationsSettings', views.EmployeeNotificationsSettings, name='EmployeeNotificationsSettings'),
    
    path('UserPayment/<int:subscription_id>', views.UserPayment, name='UserPayment'),
    path('checkPaymentProcess/<str:orderID>', views.checkPaymentProcess, name='checkPaymentProcess'),
]