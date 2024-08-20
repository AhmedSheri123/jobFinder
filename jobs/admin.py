from django.contrib import admin
from .models import JobsModel, JobAppliersModel

# Register your models here.

admin.site.register(JobsModel)
admin.site.register(JobAppliersModel)