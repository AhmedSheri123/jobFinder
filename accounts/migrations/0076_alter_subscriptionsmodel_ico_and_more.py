# Generated by Django 4.2.14 on 2024-09-16 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0075_whatsappotp_country_code_whatsappotp_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionsmodel',
            name='ico',
            field=models.ImageField(upload_to='subscription/ico/'),
        ),
        migrations.AlterField(
            model_name='subscriptionsmodel',
            name='subtitle',
            field=models.TextField(verbose_name='العنوان الفرعي'),
        ),
    ]
