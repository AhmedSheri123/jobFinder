from django.db import models

# Create your models here.

class GeneralSettingsModel(models.Model):
    about = models.TextField(blank=True, null=True, verbose_name="نبذة عن المنصة")
    img = models.ImageField(upload_to='site/img/%Y/%m/')


    phone = models.CharField(max_length=250, default='', blank=True, null=True, verbose_name="phone")
    email = models.CharField(max_length=250, default='', blank=True, null=True, verbose_name="email")
    facebook = models.CharField(max_length=250, default='', blank=True, null=True, verbose_name="facebook")
    linkedin = models.CharField(max_length=250, default='', blank=True, null=True, verbose_name="linkedin")
    whatsapp = models.CharField(max_length=250, default='', blank=True, null=True, verbose_name="whatsapp")
    instgram = models.CharField(max_length=250, default='', blank=True, null=True, verbose_name="instgram")
    snapshat = models.CharField(max_length=250, default='', blank=True, null=True, verbose_name="snapshat")
    tiktok = models.CharField(max_length=250, default='', blank=True, null=True, verbose_name="tiktok")

    allow_company_signup = models.BooleanField('السماح للشركات التسجيل', default=True)