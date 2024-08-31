from django.contrib import admin
from .models import UserProfile, EmployeeProfile, CountrysModel, SkilsModel, CompanyProfile, NotificationsModel, SubscriptionsModel, UserSubscriptionModel, UserViewedProfileModel, AdminADSModel, ForgetPWDModel

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(EmployeeProfile)
admin.site.register(CountrysModel)
admin.site.register(SkilsModel)
admin.site.register(CompanyProfile)
admin.site.register(NotificationsModel)
admin.site.register(SubscriptionsModel)
admin.site.register(UserSubscriptionModel)
admin.site.register(UserViewedProfileModel)
admin.site.register(AdminADSModel)
admin.site.register(ForgetPWDModel)