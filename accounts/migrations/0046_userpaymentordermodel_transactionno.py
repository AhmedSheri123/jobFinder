# Generated by Django 4.2.14 on 2024-08-24 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0045_userpaymentordermodel_is_buyed'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpaymentordermodel',
            name='transactionNo',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
