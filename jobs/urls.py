from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='JobIndex'),
    path('viewJob/<int:id>', views.viewJob, name='viewJob'),
]