# Generated by Django 4.2.14 on 2024-09-19 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0083_alter_subscriptionsmodel_referral_percentage_earn'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionsmodel',
            name='apply_jobs',
            field=models.BooleanField(default=False, verbose_name='التقديم على الوظائف'),
        ),
    ]