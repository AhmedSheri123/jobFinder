# Generated by Django 4.2.14 on 2024-09-01 22:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0058_alter_countrysmodel_name_adminpermissionmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminadsmodel',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.countrysmodel', verbose_name='الدولة'),
        ),
        migrations.AlterField(
            model_name='subscriptionpricebycountry',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.countrysmodel', verbose_name='الدولة'),
        ),
    ]