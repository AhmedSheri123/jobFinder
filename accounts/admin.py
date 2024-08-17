from django.contrib import admin
from .models import UserProfile, EmployeeProfile, CountrysModel, SkilsModel, CompanyProfile, NotificationsModel

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(EmployeeProfile)
admin.site.register(CountrysModel)
admin.site.register(SkilsModel)
admin.site.register(CompanyProfile)
admin.site.register(NotificationsModel)