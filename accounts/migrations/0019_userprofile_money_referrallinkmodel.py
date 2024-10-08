# Generated by Django 4.2.14 on 2024-08-17 23:32

import accounts.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_notificationsmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='money',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=6, verbose_name='الرصيد'),
        ),
        migrations.CreateModel(
            name='ReferralLinkModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referral_id', models.CharField(blank=True, default=accounts.models.GenrateRefString, max_length=250, null=True)),
                ('total_earn', models.DecimalField(blank=True, decimal_places=3, default=0.0, max_digits=6, null=True)),
                ('withdraw_earn', models.DecimalField(blank=True, decimal_places=3, default=0.0, max_digits=6, null=True)),
                ('all_total_earn', models.DecimalField(blank=True, decimal_places=3, default=0.0, max_digits=6, null=True)),
                ('percentage_of_withdraw', models.IntegerField(blank=True, null=True)),
                ('add_balance_for_signup', models.BooleanField(default=False, verbose_name='اضافة رصيد للمنشاء الحساب')),
                ('add_balance_for_signup_amount', models.DecimalField(blank=True, decimal_places=3, default=0.0, max_digits=6, null=True, verbose_name='كمية اضافة رصيد للمنشاء الحساب')),
                ('creator_userprofile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile')),
            ],
        ),
    ]
