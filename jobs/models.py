from django.db import models
from accounts.company_field import CompanyGenderFields
from accounts.fields import CertTypeFields, JobTypeFields
from django.contrib.auth.models import User
from accounts.libs import when_published

# Create your models here.



JobProcessChoices = (
    ("1", "تم التقديم"),
    ("2", "مقبول"),
    ("3", "مرفوض"),
)

JobStateChoices = (
    ("0", "قيد المراجعة"),
    ("1", "مفتوح"),
    ("2", "مغلق"),
    ("3", "اخفاء"),
)

class JobsModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    job_title = models.CharField(max_length=50, null=True, verbose_name="المسمى الوظيفي")
    monthly_salary = models.CharField(max_length=50, null=True, verbose_name="الراتب الشهري")
    cert_type = models.CharField(max_length=255, choices = CertTypeFields, null=True, verbose_name="المؤهل المطلوب")
    experiences = models.TextField(verbose_name="الخبرات المطلوبة")
    gender = models.CharField(max_length=255, choices=CompanyGenderFields, null=True, verbose_name="الجنس")
    age_from = models.IntegerField(verbose_name="العمر من")
    age_to = models.IntegerField(verbose_name="العمر الى")

    job_type = models.CharField(max_length=255, choices=JobTypeFields, null=True, verbose_name="الجنس")

    number_of_days_closing_job = models.IntegerField(verbose_name="عدد الايام للاغلاق الوظيفة تلقائيا", default=30)
    about_job = models.TextField(verbose_name="نبذه مختصرة عن مهام الوظيفة")
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")

    has_complited = models.BooleanField(default=False, verbose_name='تم مراجعتها من قبل')
    state = models.CharField(max_length=255, choices = JobStateChoices, default='0', null=True, verbose_name="المؤهل المطلوب")
    def __str__(self):
        return str(self.user.username)
    
    def whenpublished(self):
        return when_published(self.creation_date)
    

class JobAppliersModel(models.Model):
    user = models.ForeignKey(User, verbose_name="المتقدم", on_delete=models.CASCADE)
    job = models.ForeignKey(JobsModel, verbose_name="الوظيفة", on_delete=models.CASCADE)
    msg = models.TextField(null=True)

    state = models.CharField(max_length=255, choices = JobProcessChoices, default='1', null=True, verbose_name="المؤهل المطلوب")
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")

    def __str__(self):
        return str(self.user.username)
    
    def whenpublished(self):
        return when_published(self.creation_date)