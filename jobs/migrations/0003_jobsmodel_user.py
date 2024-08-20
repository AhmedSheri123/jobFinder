# Generated by Django 4.2.14 on 2024-08-19 20:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0002_jobsmodel_state_alter_jobappliersmodel_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobsmodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
