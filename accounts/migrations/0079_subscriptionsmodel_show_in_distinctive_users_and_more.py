# Generated by Django 4.2.14 on 2024-09-17 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0078_whatsappotp_email_alter_subscriptionsmodel_ico_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionsmodel',
            name='show_in_distinctive_users',
            field=models.BooleanField(default=False, verbose_name='الظهور ضمن الاعضاء التميز'),
        ),
        migrations.AddField(
            model_name='subscriptionsmodel',
            name='show_on_first_search',
            field=models.BooleanField(default=False, verbose_name='الظهور في مقدمة البحث'),
        ),
    ]
