# Generated by Django 4.2.14 on 2024-08-18 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_alter_userprofile_admin_permission'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewersCounterByIPADDR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_addr', models.CharField(max_length=255)),
                ('creation_date', models.DateTimeField(null=True, verbose_name='تاريخ الانشاء')),
            ],
        ),
    ]
