# Generated by Django 4.2.14 on 2024-09-03 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0065_alter_employeeprofile_skils'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeprofile',
            name='skils',
            field=models.JSONField(default=dict, null=True, verbose_name='مهارات json'),
        ),
    ]
