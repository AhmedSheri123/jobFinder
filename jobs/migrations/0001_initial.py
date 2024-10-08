# Generated by Django 4.2.14 on 2024-08-18 00:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JobsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=50, null=True, verbose_name='المسمى الوظيفي')),
                ('monthly_salary', models.CharField(max_length=50, null=True, verbose_name='الراتب الشهري')),
                ('cert_type', models.CharField(choices=[('1', 'المرحلة الثانوية'), ('2', 'دبلوم'), ('3', 'البكالوريوس'), ('4', 'ماجستير'), ('5', 'دكتوراة')], max_length=255, null=True, verbose_name='المؤهل المطلوب')),
                ('experiences', models.TextField(verbose_name='الخبرات المطلوبة')),
                ('gender', models.CharField(choices=[('1', 'ذكر'), ('2', 'انثى'), ('3', 'الجنسين')], max_length=255, null=True, verbose_name='الجنس')),
                ('age_from', models.IntegerField(verbose_name='العمر من')),
                ('age_to', models.IntegerField(verbose_name='العمر الى')),
                ('number_of_days_closing_job', models.IntegerField(verbose_name='عدد الايام للاغلاق الوظيفة تلقائيا')),
                ('about_job', models.TextField(verbose_name='نبذه مختصرة عن مهام الوظيفة')),
                ('creation_date', models.DateTimeField(null=True, verbose_name='تاريخ الانشاء')),
            ],
        ),
        migrations.CreateModel(
            name='JobAppliersModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('0', 'المسؤول'), ('1', 'مسؤول التوظيف')], default=0, max_length=255, null=True, verbose_name='المؤهل المطلوب')),
                ('creation_date', models.DateTimeField(null=True, verbose_name='تاريخ الانشاء')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.jobsmodel', verbose_name='الوظيفة')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='المتقدم')),
            ],
        ),
    ]
