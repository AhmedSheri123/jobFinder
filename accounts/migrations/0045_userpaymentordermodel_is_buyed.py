# Generated by Django 4.2.14 on 2024-08-24 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0044_remove_userpaymentordermodel_card_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpaymentordermodel',
            name='is_buyed',
            field=models.BooleanField(default=False),
        ),
    ]
