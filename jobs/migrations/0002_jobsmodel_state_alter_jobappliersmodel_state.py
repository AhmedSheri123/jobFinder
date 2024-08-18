# Generated by Django 4.2.14 on 2024-08-18 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobsmodel',
            name='state',
            field=models.CharField(choices=[('1', 'مفتوح'), ('2', 'مغلق'), ('3', 'اخفاء')], default=0, max_length=255, null=True, verbose_name='المؤهل المطلوب'),
        ),
        migrations.AlterField(
            model_name='jobappliersmodel',
            name='state',
            field=models.CharField(choices=[('1', 'تم التقديم'), ('2', 'مقبول'), ('3', 'التقديم مغلق')], default=0, max_length=255, null=True, verbose_name='المؤهل المطلوب'),
        ),
    ]
