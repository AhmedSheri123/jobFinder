# Generated by Django 4.2.14 on 2024-08-21 00:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_subscriptions_theem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscriptions',
            old_name='distinctive',
            new_name='distinctive_frame',
        ),
    ]
