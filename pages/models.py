from django.db import models

# Create your models here.

class ContactUsModel(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    msg = models.TextField()
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")
