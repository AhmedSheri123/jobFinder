# Generated by Django 4.2.14 on 2024-08-21 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_rename_daily_number_of_receive_msgs_subscriptionsmodel_number_of_receive_msgs_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersubscriptionmodel',
            name='used_number_of_receive_msgs',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='usersubscriptionmodel',
            name='used_number_of_send_msgs',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='usersubscriptionmodel',
            name='used_number_of_view_profiles',
            field=models.IntegerField(default=1),
        ),
    ]
