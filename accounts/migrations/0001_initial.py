# Generated by Django 4.2.14 on 2024-08-06 07:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=250, null=True, verbose_name='اسم المنشئة')),
                ('complite_name', models.CharField(max_length=250, null=True, verbose_name='اسم مقدم الطلب')),
                ('phone', models.CharField(max_length=250, null=True, verbose_name='الهاتف')),
                ('employee_city', models.CharField(choices=[('1', 'ابها'), ('2', 'ابو عريش'), ('3', 'احد المسارحة'), ('4', 'الأفلاج'), ('5', 'الاحساء'), ('6', 'الارطاوية'), ('7', 'الباحة'), ('8', 'البكيرية'), ('9', 'الثقبة'), ('10', 'الجبيل'), ('11', 'الخبر'), ('12', 'الخرج'), ('13', 'الخفجي'), ('14', 'الدلم'), ('15', 'الدمام'), ('16', 'الدوادمي'), ('17', 'الرس'), ('18', 'الرقعي'), ('19', 'الرياض'), ('20', 'الزلفي'), ('21', 'السليل'), ('22', 'الطائف'), ('23', 'العلا'), ('24', 'الغاط'), ('25', 'القريات'), ('26', 'القطيف'), ('27', 'القويعية'), ('28', 'المجمعه'), ('29', 'المدينة المنورة'), ('30', 'المذنب'), ('31', 'المزاحمية'), ('32', 'النعيرية'), ('33', 'النماص'), ('34', 'الهفوف'), ('35', 'املج'), ('36', 'بدر'), ('37', 'بريدة'), ('38', 'بقيق'), ('39', 'بلجرشي'), ('40', 'بيشة'), ('41', 'تبوك'), ('42', 'جازان'), ('43', 'جدة'), ('44', 'حائل'), ('45', 'حفر الباطن'), ('46', 'حقل'), ('47', 'حوطة سدير'), ('48', 'خميس مشيط'), ('49', 'خيبر'), ('50', 'دومة الجندل'), ('51', 'رابغ'), ('52', 'رياض الخبراء'), ('53', 'سبت العلايا'), ('54', 'سكاكا'), ('55', 'شرورة'), ('56', 'شقراء'), ('57', 'صبيا'), ('58', 'ضباء'), ('59', 'ضرما'), ('60', 'طريف'), ('61', 'عرعر'), ('62', 'عنيزة'), ('63', 'قرية العليا'), ('64', 'محايل عسير'), ('65', 'مكة المكرمة'), ('66', 'نجران'), ('67', 'وادي الدواسر'), ('68', 'ينبع')], max_length=255, null=True, verbose_name='المدينة')),
                ('district', models.CharField(max_length=250, null=True, verbose_name='الحي')),
                ('land_line_number', models.CharField(max_length=250, null=True, verbose_name='هاتف ارضي')),
                ('facebook_profile', models.CharField(max_length=250, null=True, verbose_name='صفحة فيسبوك')),
                ('linkedin', models.CharField(max_length=250, null=True, verbose_name='صفحة لينكداين')),
                ('whatsapp', models.CharField(max_length=250, null=True, verbose_name='واتساب')),
                ('creation_date', models.DateTimeField(null=True, verbose_name='تاريخ الانشاء')),
            ],
        ),
        migrations.CreateModel(
            name='CountrysModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='اسم الدولة')),
                ('creation_date', models.DateTimeField(null=True, verbose_name='تاريخ الانشاء')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, null=True, verbose_name='الاسم الثلاثي')),
                ('gender', models.CharField(choices=[('1', 'ذكر'), ('2', 'انثى')], max_length=255, null=True, verbose_name='الجنس')),
                ('age', models.IntegerField(null=True, verbose_name='العمر')),
                ('weight', models.IntegerField(verbose_name='الوزن')),
                ('height', models.IntegerField(verbose_name='الطول')),
                ('marital_status', models.CharField(choices=[('0', 'اعزب'), ('1', 'متزوج')], max_length=255, null=True, verbose_name='الحالة الإجتماعية')),
                ('health_status', models.CharField(choices=[('0', 'اعزب'), ('1', 'متزوج')], max_length=255, null=True, verbose_name='الحالة الصحية')),
                ('phone', models.CharField(max_length=250, null=True, verbose_name='الهاتف')),
                ('employee_city', models.CharField(choices=[('1', 'ابها'), ('2', 'ابو عريش'), ('3', 'احد المسارحة'), ('4', 'الأفلاج'), ('5', 'الاحساء'), ('6', 'الارطاوية'), ('7', 'الباحة'), ('8', 'البكيرية'), ('9', 'الثقبة'), ('10', 'الجبيل'), ('11', 'الخبر'), ('12', 'الخرج'), ('13', 'الخفجي'), ('14', 'الدلم'), ('15', 'الدمام'), ('16', 'الدوادمي'), ('17', 'الرس'), ('18', 'الرقعي'), ('19', 'الرياض'), ('20', 'الزلفي'), ('21', 'السليل'), ('22', 'الطائف'), ('23', 'العلا'), ('24', 'الغاط'), ('25', 'القريات'), ('26', 'القطيف'), ('27', 'القويعية'), ('28', 'المجمعه'), ('29', 'المدينة المنورة'), ('30', 'المذنب'), ('31', 'المزاحمية'), ('32', 'النعيرية'), ('33', 'النماص'), ('34', 'الهفوف'), ('35', 'املج'), ('36', 'بدر'), ('37', 'بريدة'), ('38', 'بقيق'), ('39', 'بلجرشي'), ('40', 'بيشة'), ('41', 'تبوك'), ('42', 'جازان'), ('43', 'جدة'), ('44', 'حائل'), ('45', 'حفر الباطن'), ('46', 'حقل'), ('47', 'حوطة سدير'), ('48', 'خميس مشيط'), ('49', 'خيبر'), ('50', 'دومة الجندل'), ('51', 'رابغ'), ('52', 'رياض الخبراء'), ('53', 'سبت العلايا'), ('54', 'سكاكا'), ('55', 'شرورة'), ('56', 'شقراء'), ('57', 'صبيا'), ('58', 'ضباء'), ('59', 'ضرما'), ('60', 'طريف'), ('61', 'عرعر'), ('62', 'عنيزة'), ('63', 'قرية العليا'), ('64', 'محايل عسير'), ('65', 'مكة المكرمة'), ('66', 'نجران'), ('67', 'وادي الدواسر'), ('68', 'ينبع')], max_length=255, null=True, verbose_name='المدينة')),
                ('district', models.CharField(max_length=250, null=True, verbose_name='الحي')),
                ('nationality', models.CharField(choices=[('1', 'سعودي'), ('2', 'غير سعودي')], max_length=255, null=True, verbose_name='الجنسية')),
                ('how_hear', models.CharField(choices=[('1', 'صديق'), ('2', 'الجمعيات الداعمة للأشخاص ذوي الإعاقة'), ('3', 'منصات التواصل الإجتماعي'), ('0', 'اخرى')], max_length=255, null=True, verbose_name='كيف سمعت عنا')),
                ('how_hear_other', models.CharField(max_length=250, null=True, verbose_name='اذكر لنا كيف سمعت عنا')),
                ('have_car', models.CharField(choices=[('0', 'لا'), ('1', 'نعم')], max_length=255, null=True, verbose_name='أمتلك سيارة ورخصة قيادة')),
                ('about_me', models.TextField(verbose_name='نبذة عني')),
                ('desires', models.JSONField(verbose_name='الرغبات json')),
                ('major', models.CharField(max_length=250, null=True, verbose_name='التخصص الدراسي')),
                ('job_title', models.CharField(max_length=50, null=True, verbose_name='المسمى الوظيفي')),
                ('cert_type', models.CharField(choices=[('1', 'المرحلة الثانوية'), ('2', 'دبلوم'), ('3', 'البكالوريوس'), ('4', 'ماجستير'), ('5', 'دكتوراة')], max_length=255, null=True, verbose_name='نوع الشهادة')),
                ('learning_domain', models.CharField(choices=[('1', 'كلية الاقتصاد والإدارة'), ('2', 'معهد الاقتصاد الإسلامي'), ('3', 'كلية الآداب والعلوم الإنسانية'), ('4', 'معهد اللغة الإنجليزية'), ('5', 'كلية العلوم'), ('6', 'كلية الهندسة'), ('7', 'كلية العمارة والتخطيط'), ('8', 'كلية الطب'), ('9', 'كلية العلوم التطبيقية'), ('10', 'كلية علوم الأرض'), ('11', 'كلية علوم البحار'), ('12', 'كلية الحقوق'), ('13', 'كلية العلوم البيئية'), ('16', 'كلية الصيدلة'), ('18', 'كلية السياحة'), ('19', 'كلية علوم الانسان والتصاميم'), ('21', 'كلية التربية'), ('22', 'كلية الاتصال والإعلام'), ('24', 'كلية الحاسبات وتقنية المعلومات'), ('25', 'كلية التمريض'), ('0', 'أخرى')], max_length=255, null=True, verbose_name='مجال التعلم')),
                ('cv', models.FileField(upload_to='employee_cv/%Y/%m/%d/')),
                ('employee_password', models.CharField(max_length=250, null=True, verbose_name='كلمة المرور للمنصة')),
                ('creation_date', models.DateTimeField(null=True, verbose_name='تاريخ الانشاء')),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.countrysmodel', verbose_name='الدولة')),
            ],
        ),
        migrations.CreateModel(
            name='SkilsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='اسم المهارة')),
                ('creation_date', models.DateTimeField(null=True, verbose_name='تاريخ الانشاء')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_employee', models.BooleanField(default=False, null=True, verbose_name='هل هو موظف')),
                ('is_company', models.BooleanField(default=False, null=True, verbose_name='هل هو شركة')),
                ('admin_permission', models.CharField(blank=True, choices=[('0', 'المسؤول'), ('1', 'مسؤول التوظيف')], max_length=255, null=True, verbose_name='الاذونات')),
                ('creation_date', models.DateTimeField(null=True, verbose_name='تاريخ الانشاء')),
                ('is_email_verificated', models.BooleanField(default=False, null=True, verbose_name='هل تم تأكيد بريد الالكتروني')),
                ('is_phone_verificated', models.BooleanField(default=False, null=True, verbose_name='هل تم تأكيد الرقم')),
                ('companyprofile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.companyprofile')),
                ('employeeprofile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.employeeprofile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='skils',
            field=models.ManyToManyField(to='accounts.skilsmodel', verbose_name='المهارات'),
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.countrysmodel', verbose_name='الدولة'),
        ),
    ]
