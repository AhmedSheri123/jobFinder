from django.urls import path
from . import views

urlpatterns = [
    path('PanelHome', views.PanelHome, name='PanelHome'),

    #Employee
    path('PanelShowEmployees', views.PanelShowEmployees, name='PanelShowEmployees'),
    path('PanelShowEmployee/<int:id>', views.PanelShowEmployee, name='PanelShowEmployee'),
    path('DeleteEmployees/<int:id>', views.DeleteEmployees, name='DeleteEmployees'),


    #Company
    path('Companys', views.Companys, name='Companys'),
    path('Company/<int:id>', views.Company, name='Company'),
    path('DeleteCompanys/<int:id>', views.DeleteCompanys, name='DeleteCompanys'),

    #Jobs
    path('ViewJobsPanel', views.ViewJobsPanel, name='ViewJobsPanel'),
    path('ViewCompanyPostJobs/<int:id>', views.ViewCompanyPostJobs, name='ViewCompanyPostJobs'),
    path('adminDeleteAppier/<int:id>', views.adminDeleteAppier, name='adminDeleteAppier'),
    path('adminDeleteJob/<int:id>', views.adminDeleteJob, name='adminDeleteJob'),

    #Subscriptions
    path('PanelViewSubscriptions', views.PanelViewSubscriptions, name='PanelViewSubscriptions'),
    path('PanelAddSubscriptions', views.PanelAddSubscriptions, name='PanelAddSubscriptions'),
    path('PanelEditSubscriptions/<int:id>', views.PanelEditSubscriptions, name='PanelEditSubscriptions'),
    path('PanelDeleteSubscriptions/<int:id>', views.PanelDeleteSubscriptions, name='PanelDeleteSubscriptions'),


    path('ManageSubscriptionPriceByCountry', views.ManageSubscriptionPriceByCountry, name='ManageSubscriptionPriceByCountry'),
    path('AddSubscriptionPriceByCountry', views.AddSubscriptionPriceByCountry, name='AddSubscriptionPriceByCountry'),
    path('EditSubscriptionPriceByCountry/<int:id>', views.EditSubscriptionPriceByCountry, name='EditSubscriptionPriceByCountry'),
    path('DeleteSubscriptionPriceByCountry/<int:id>', views.DeleteSubscriptionPriceByCountry, name='DeleteSubscriptionPriceByCountry'),
    


    path('ShowAllContactUsHistory', views.ShowAllContactUsHistory, name='ShowAllContactUsHistory'),
    path('DeleteContactUs/<int:id>', views.DeleteContactUs, name='DeleteContactUs'),


    #ADS
    path('ManageAdminADS', views.ManageAdminADS, name='ManageAdminADS'),
    path('AddAdminADS', views.AddAdminADS, name='AddAdminADS'),
    path('EditAdminADS/<int:id>', views.EditAdminADS, name='EditAdminADS'),
    path('DeleteAdminADS/<int:id>', views.DeleteAdminADS, name='DeleteAdminADS'),
    

    #countrys
    path('ManageCountrys', views.ManageCountrys, name='ManageCountrys'),
    path('AddCountrys', views.AddCountrys, name='AddCountrys'),
    path('EditCountrys/<int:id>', views.EditCountrys, name='EditCountrys'),
    path('DeleteCountrys/<int:id>', views.DeleteCountrys, name='DeleteCountrys'),
    

    #nationality
    path('ManageNationality', views.ManageNationality, name='ManageNationality'),
    path('AddNationality', views.AddNationality, name='AddNationality'),
    path('EditNationality/<int:id>', views.EditNationality, name='EditNationality'),
    path('DeleteNationality/<int:id>', views.DeleteNationality, name='DeleteNationality'),
    

    #HealthStatus
    path('ManageHealthStatus', views.ManageHealthStatus, name='ManageHealthStatus'),
    path('AddHealthStatus', views.AddHealthStatus, name='AddHealthStatus'),
    path('EditHealthStatus/<int:id>', views.EditHealthStatus, name='EditHealthStatus'),
    path('DeleteHealthStatus/<int:id>', views.DeleteHealthStatus, name='DeleteHealthStatus'),
    

    #AdminPermission
    path('ManageAdminPermission', views.ManageAdminPermission, name='ManageAdminPermission'),
    path('AddAdminPermission', views.AddAdminPermission, name='AddAdminPermission'),
    path('EditAdminPermission/<int:id>', views.EditAdminPermission, name='EditAdminPermission'),
    path('DeleteAdminPermission/<int:id>', views.DeleteAdminPermission, name='DeleteAdminPermission'),

    path('EditVerificationMsg', views.EditVerificationMsg, name='EditVerificationMsg'),
    path('EditTermsPolicy', views.EditTermsPolicy, name='EditTermsPolicy'),
    
    

    
    path('WithdrawDelete/<int:id>', views.WithdrawDelete, name='WithdrawDelete'),
    path('WithdrawComplete/<int:id>', views.WithdrawComplete, name='WithdrawComplete'),
    path('WithdrawCancel/<int:id>', views.WithdrawCancel, name='WithdrawCancel'),
    path('WithdrawAccept/<int:id>', views.WithdrawAccept, name='WithdrawAccept'),
    path('dashboardWithdraw', views.dashboardWithdraw, name='dashboardWithdraw'),



    path('ContactUsSendReplay/<int:id>', views.ContactUsSendReplay, name='ContactUsSendReplay'),

    path('ManageJobSalaries', views.ManageJobSalaries, name='ManageJobSalaries'),
    path('AddJobSalaries', views.AddJobSalaries, name='AddJobSalaries'),
    path('EditJobSalaries/<int:id>', views.EditJobSalaries, name='EditJobSalaries'),
    path('DeleteJobSalaries/<int:id>', views.DeleteJobSalaries, name='DeleteJobSalaries'),


    path('GeneralSettings', views.GeneralSettings, name='GeneralSettings'),
    path('ManageNotifications', views.ManageNotifications, name='ManageNotifications'),
    path('DeleteNotifications/<int:id>', views.DeleteNotifications, name='DeleteNotifications'),
]