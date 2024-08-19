from django.urls import path
from . import views

urlpatterns = [
    #Employee
    path('PanelHome', views.PanelHome, name='PanelHome'),
    path('PanelShowEmployees', views.PanelShowEmployees, name='PanelShowEmployees'),
    path('PanelShowEmployee/<int:id>', views.PanelShowEmployee, name='PanelShowEmployee'),
    path('DeleteEmployees/<int:id>', views.DeleteEmployees, name='DeleteEmployees'),


    #Company
    path('Companys', views.Companys, name='Companys'),
    path('Company/<int:id>', views.Company, name='Company'),
    path('DeleteCompanys/<int:id>', views.DeleteCompanys, name='DeleteCompanys'),

]