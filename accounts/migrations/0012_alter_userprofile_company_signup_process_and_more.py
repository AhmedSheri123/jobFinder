# Generated by Django 4.2.14 on 2024-08-11 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_userprofile_company_signup_process_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='company_signup_process',
            field=models.CharField(choices=[('0', 'ملغي'), ('1', 'إنشاء حساب'), ('2', 'تاكيد الحساب'), ('3', 'إعداد ملف شخصي'), ('4', 'قيد المراجعة'), ('5', 'مكتمل')], default='1', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='cv_signup_process',
            field=models.CharField(choices=[('0', 'ملغي'), ('1', 'إنشاء حساب'), ('2', 'تاكيد الحساب'), ('3', 'إعداد ملف شخصي'), ('4', 'بناء سيرتك الذاتية'), ('5', 'قيد المراجعة'), ('6', 'مكتمل')], default='1', max_length=255, null=True),
        ),
    ]
