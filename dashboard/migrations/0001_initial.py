# Generated by Django 4.2.14 on 2024-09-19 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralSettingsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.TextField(blank=True, null=True, verbose_name='نبذة عن المنصة')),
                ('img', models.ImageField(upload_to='site/img/%Y/%m/')),
                ('facebook', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='facebook')),
                ('linkedin', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='linkedin')),
                ('whatsapp', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='whatsapp')),
                ('instgram', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='instgram')),
                ('snapshat', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='snapshat')),
                ('tiktok', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='tiktok')),
            ],
        ),
    ]
