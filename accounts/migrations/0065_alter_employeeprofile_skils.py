# Generated by Django 4.2.14 on 2024-09-03 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0064_employeeprofile_classes_employeeprofile_experiences_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeprofile',
            name='skils',
            field=models.TextField(null=True, verbose_name='المهارات'),
        ),
    ]
