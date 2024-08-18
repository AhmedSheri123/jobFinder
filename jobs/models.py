from django.db import models
from accounts.company_field import CompanyGenderFields
from accounts.fields import CertTypeFields
from django.contrib.auth.models import User

# Create your models here.



JobProcessChoices = (
    ("1", "تم التقديم"),
    ("2", "مقبول"),
    ("3", "التقديم مغلق"),
)

JobStateChoices = (
    ("1", "مفتوح"),
    ("2", "مغلق"),
    ("3", "اخفاء"),
)

class JobsModel(models.Model):
    job_title = models.CharField(max_length=50, null=True, verbose_name="المسمى الوظيفي")
    monthly_salary = models.CharField(max_length=50, null=True, verbose_name="الراتب الشهري")
    cert_type = models.CharField(max_length=255, choices = CertTypeFields, null=True, verbose_name="المؤهل المطلوب")
    experiences = models.TextField(verbose_name="الخبرات المطلوبة")
    gender = models.CharField(max_length=255, choices=CompanyGenderFields, null=True, verbose_name="الجنس")
    age_from = models.IntegerField(verbose_name="العمر من")
    age_to = models.IntegerField(verbose_name="العمر الى")

    number_of_days_closing_job = models.IntegerField(verbose_name="عدد الايام للاغلاق الوظيفة تلقائيا")
    about_job = models.TextField(verbose_name="نبذه مختصرة عن مهام الوظيفة")
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")
    state = models.CharField(max_length=255, choices = JobStateChoices, default=0, null=True, verbose_name="المؤهل المطلوب")

class JobAppliersModel(models.Model):
    user = models.ForeignKey(User, verbose_name="المتقدم", on_delete=models.CASCADE)
    job = models.ForeignKey(JobsModel, verbose_name="الوظيفة", on_delete=models.CASCADE)

    state = models.CharField(max_length=255, choices = JobProcessChoices, default=0, null=True, verbose_name="المؤهل المطلوب")
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")