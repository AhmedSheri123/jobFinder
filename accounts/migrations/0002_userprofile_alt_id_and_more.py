# Generated by Django 4.2.14 on 2024-08-08 22:17

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='alt_id',
            field=models.CharField(default=accounts.models.StrNumCodeGen, max_length=255),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='employee_city',
            field=models.CharField(max_length=255, null=True, verbose_name='المدينة'),
        ),
    ]
