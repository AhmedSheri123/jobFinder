# Generated by Django 4.2.14 on 2024-08-21 00:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_rename_distinctive_subscriptions_distinctive_frame'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Subscriptions',
            new_name='SubscriptionsModel',
        ),
        migrations.CreateModel(
            name='UserSubscriptionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_days', models.IntegerField(default=30)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('daily_number_of_receive_msgs', models.IntegerField(default=1)),
                ('daily_number_of_send_msgs', models.IntegerField(default=1)),
                ('number_of_view_profiles', models.IntegerField(default=1)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.subscriptionsmodel')),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='subscription',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.usersubscriptionmodel'),
        ),
    ]
