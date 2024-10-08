# Generated by Django 4.2.14 on 2024-08-21 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0038_employeeprofile_instgram_employeeprofile_snapshat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyprofile',
            name='instgram',
            field=models.CharField(max_length=250, null=True, verbose_name='instgram'),
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='snapshat',
            field=models.CharField(max_length=250, null=True, verbose_name='snapshat'),
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='tiktok',
            field=models.CharField(max_length=250, null=True, verbose_name='tiktok'),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='instgram',
            field=models.CharField(max_length=250, null=True, verbose_name='instgram'),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='whatsapp',
            field=models.CharField(max_length=250, null=True, verbose_name='whatsapp'),
        ),
    ]
