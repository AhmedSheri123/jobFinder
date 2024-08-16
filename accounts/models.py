from django.db import models
from .fields import HealthStatusFields, EmployeePostStateFields, citys, StateFields, YesNoFields, NationalityFields, GenderFields, HowHearFields, CertTypeFields, JobTypeFields, JobPropertiesFields, LanguageLevelFields, LearningDomainFields
from django.contrib.auth.models import User
from .company_field import CompanyHaveCertFields, CompanySectionFields, CompanySizeFields, CompanyGenderFields, CompanyWorktimeFields, PostStateFields, CertTypeFieldsCompany
from django.utils import timezone
import math
import string
import random
from messenger.models import MessengerModel

# Create your models here.
AdminPermission = (
    ("0", "المسؤول"),
    ("1", "مسؤول التوظيف"),
    # ("2", "المجند"),
)

CVSignupProcessChoices = (
    ("0", "ملغي"),
    ("1", "إنشاء حساب"),
    ("2", "تاكيد الحساب"),
    ("3", "إعداد ملف شخصي"),
    ("4", "بناء سيرتك الذاتية"),
    ("5", "قيد المراجعة"),
    ("6", "مكتمل"),
)

CompanySignupProcessChoices = (
    ("0", "ملغي"),
    ("1", "إنشاء حساب"),
    ("2", "إعداد ملف شخصي"),
    ("3", "تاكيد الحساب"),
    ("4", "قيد المراجعة"),
    ("5", "مكتمل"),
)

def EmployeeRandomNumCodeGen():
    N = 4
    res = ''.join(random.choices(string.digits, k=N))
    return 'i' + str(res)

def CompanyRandomNumCodeGen():
    N = 4
    res = ''.join(random.choices(string.digits, k=N))
    return 'o' + str(res)

def StrNumCodeGen():
    N = 13
    res = ''.join(random.choices(string.digits+ string.ascii_letters, k=N))
    return str(res)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_employee = models.BooleanField(default=False, null=True, verbose_name="هل هو موظف")
    is_company = models.BooleanField(default=False, null=True, verbose_name="هل هو شركة")

    employeeprofile = models.ForeignKey('EmployeeProfile', on_delete=models.CASCADE, null=True, blank=True)
    companyprofile = models.ForeignKey('CompanyProfile', on_delete=models.CASCADE, null=True, blank=True)

    admin_permission = models.CharField(max_length=255, choices = AdminPermission, null=True, blank=True, verbose_name="الاذونات")
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")

    is_email_verificated = models.BooleanField(default=False, null=True, verbose_name="هل تم تأكيد بريد الالكتروني")
    is_phone_verificated = models.BooleanField(default=False, null=True, verbose_name="هل تم تأكيد الرقم")

    company_signup_process = models.CharField(default='1', max_length=255, choices = CompanySignupProcessChoices, null=True)
    cv_signup_process = models.CharField(default='1', max_length=255, choices = CVSignupProcessChoices, null=True)

    alt_id = models.CharField(max_length=255, default=StrNumCodeGen)

    is_active = models.BooleanField(default=False)
    last_active_datetime = models.DateTimeField(null=True, blank=True)
    
    is_in_chat = models.BooleanField(default=False)
    active_messenger = models.ForeignKey(MessengerModel, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

class CountrysModel(models.Model):
    name = models.CharField(max_length=255, null=True, verbose_name="اسم الدولة")
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")
    def __str__(self):
        return self.name
class SkilsModel(models.Model):
    name = models.CharField(max_length=255, null=True, verbose_name="اسم المهارة")
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")
    

    def __str__(self):
        return self.name
    
    
class EmployeeProfile(models.Model):
    name = models.CharField(max_length=250, null=True, verbose_name="الاسم الثلاثي")
    gender = models.CharField(max_length=255, choices = GenderFields, null=True, verbose_name="الجنس")
    age = models.IntegerField(null=True, verbose_name="العمر")
    weight = models.IntegerField(verbose_name="الوزن", null=True)
    height = models.IntegerField(verbose_name="الطول", null=True)
    marital_status = models.CharField(max_length=255, choices = StateFields, null=True, verbose_name="الحالة الإجتماعية")
    health_status = models.CharField(max_length=255, choices = HealthStatusFields, null=True, verbose_name="الحالة الصحية")
    phone = models.CharField(max_length=250, null=True, verbose_name="الهاتف")
    country = models.ForeignKey('CountrysModel', on_delete=models.SET_NULL, null=True, verbose_name='الدولة')
    employee_city = models.CharField(max_length=255, null=True, verbose_name="المدينة")
    district = models.CharField(max_length=250, null=True, verbose_name="الحي")
    nationality = models.CharField(max_length=255, choices = NationalityFields, null=True, verbose_name="الجنسية")
    how_hear = models.CharField(max_length=255, choices = HowHearFields, null=True, verbose_name="كيف سمعت عنا")
    how_hear_other = models.CharField(max_length=250, null=True, verbose_name="اذكر لنا كيف سمعت عنا")
    have_car = models.CharField(max_length=255, choices = YesNoFields, null=True, verbose_name="أمتلك سيارة ورخصة قيادة")
    
    about_me = models.TextField(verbose_name='نبذة عني', null=True)
    desires = models.JSONField(verbose_name='الرغبات json', null=True)

    major = models.CharField(max_length=250, null=True, verbose_name="التخصص الدراسي")
    job_title = models.CharField(max_length=50, null=True, verbose_name="المسمى الوظيفي")
    skils = models.TextField(verbose_name='المهارات', null=True)

    cert_type = models.CharField(max_length=255, choices = CertTypeFields, null=True, verbose_name="نوع الشهادة")
    learning_domain = models.CharField(max_length=255, choices = LearningDomainFields, null=True, verbose_name="مجال التعلم")

    cv = models.FileField(upload_to="employee_cv/%Y/%m/%d/")
    employee_password = models.CharField(max_length=250, null=True, verbose_name="كلمة المرور للمنصة")

    facebook = models.CharField(max_length=250, null=True, verbose_name="facebook")
    linkedin = models.CharField(max_length=250, null=True, verbose_name="linkedin")
    whatsapp = models.CharField(max_length=250, null=True, verbose_name="whatsapp")

    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")
    def __str__(self):
        return str(self.name)
    

class CompanyProfile(models.Model):
    company_name = models.CharField(max_length=250, null=True, verbose_name="اسم المنشئة")
    complite_name = models.CharField(max_length=250, null=True, verbose_name="اسم مقدم الطلب")
    phone = models.CharField(max_length=250, null=True, verbose_name="الهاتف")
    about_me = models.TextField(verbose_name='نبذة عني', null=True)
    img_base64 = models.TextField(blank=True, null=True)

    country = models.ForeignKey('CountrysModel', on_delete=models.SET_NULL, null=True, verbose_name='الدولة')
    employee_city = models.CharField(max_length=255, null=True, verbose_name="المدينة")
    district = models.CharField(max_length=250, null=True, verbose_name="الحي")
    
    land_line_number = models.CharField(max_length=250, null=True, verbose_name="هاتف ارضي")
    facebook_profile = models.CharField(max_length=250, null=True, verbose_name="صفحة فيسبوك")
    linkedin = models.CharField(max_length=250, null=True, verbose_name="صفحة لينكداين")
    whatsapp = models.CharField(max_length=250, null=True, verbose_name="واتساب")



    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")
    def __str__(self):
        return str(self.company_name)
    

class EmployeeProfileImages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to="users/profile/imgs/%Y/%m/%d", blank=True, null=True)
    img_base64 = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")