# Generated by Django 4.2.14 on 2024-08-22 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0039_companyprofile_instgram_companyprofile_snapshat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='dont_receive_msg_from_companys',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='dont_receive_msg_from_employees',
            field=models.BooleanField(default=False),
        ),
    ]
