# Generated by Django 4.2.14 on 2024-09-11 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0074_remove_userprofile_phone_country_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='whatsappotp',
            name='country_code',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='whatsappotp',
            name='phone',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]