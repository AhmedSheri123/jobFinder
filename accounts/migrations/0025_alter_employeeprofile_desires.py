# Generated by Django 4.2.14 on 2024-08-20 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_viewerscounterbyipaddr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeprofile',
            name='desires',
            field=models.JSONField(default=dict, null=True, verbose_name='الرغبات json'),
        ),
    ]