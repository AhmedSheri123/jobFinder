# Generated by Django 4.2.14 on 2024-08-18 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_delete_jobappliersmodel_delete_jobsmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='admin_permission',
            field=models.CharField(blank=True, choices=[('0', 'المسؤول'), ('1', 'مسؤول التوظيف')], max_length=255, null=True, verbose_name='الاذونات'),
        ),
    ]
