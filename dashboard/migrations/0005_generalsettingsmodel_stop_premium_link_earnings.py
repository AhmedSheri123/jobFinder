# Generated by Django 4.2.14 on 2024-12-29 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_generalsettingsmodel_allow_employee_signup'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalsettingsmodel',
            name='stop_premium_link_earnings',
            field=models.BooleanField(default=False, verbose_name='ايقاف ارباح الروابط المميزة'),
        ),
    ]
