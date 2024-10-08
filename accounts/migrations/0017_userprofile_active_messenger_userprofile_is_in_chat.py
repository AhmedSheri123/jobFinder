# Generated by Django 4.2.14 on 2024-08-16 02:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0004_alter_messagesmodel_creation_date'),
        ('accounts', '0016_remove_companyprofile_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='active_messenger',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='messenger.messengermodel'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_in_chat',
            field=models.BooleanField(default=False),
        ),
    ]
