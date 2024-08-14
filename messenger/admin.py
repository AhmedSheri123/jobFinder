from django.contrib import admin
from .models import MessagesModel, MessengerModel

# Register your models here.
admin.site.register(MessagesModel)
admin.site.register(MessengerModel)