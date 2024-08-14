from django.urls import path
from . import views

urlpatterns = [
    path('messageRoom/<str:room_id>', views.messageRoom, name="messageRoom")
]