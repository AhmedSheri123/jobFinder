# Generated by Django 4.2.14 on 2024-09-19 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0081_alter_companyprofile_about_me'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionsmodel',
            name='referral_percentage_earn',
            field=models.IntegerField(default=0, verbose_name='النسبة المئوية لتسويق بلعمولة'),
        ),
    ]