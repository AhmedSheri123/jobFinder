from django.db import models
from .fields import CountrysChoices, HealthStatusFields, EmployeePostStateFields, citys, StateFields, YesNoFields, NationalityFields, GenderFields, HowHearFields, CertTypeFields, JobTypeFields, JobPropertiesFields, LanguageLevelFields, LearningDomainFields
from django.contrib.auth.models import User
from .company_field import CompanyWorktimeFields, PostStateFields, CertTypeFieldsCompany
from django.utils import timezone
import string, datetime
import random
from messenger.models import MessengerModel
from .libs import when_published, DatetimeNow
from django.urls import reverse

# Create your models here.
AdminPermission = (
    ("0", "المسؤول"),
    ("1", "مسؤول التوظيف"),
    # ("2", "المجند"),

)


CurrencyChoices = (
    ("SAR", "ريال سعودي"),
    ("USD", "دولار"),
    ("EUR", "يورو"),
)

# CountryChoices = (
#     ("SA", "السعودية"),
#     ("USA", "ولايات المتحدة الامريكية"),
#     ("SY", "سوريا"),
#     ("EG", "مصر"),
# )



CVSignupProcessChoices = (
    ("0", "ملغي"),
    ("1", "إنشاء حساب"),
    ("2", "تاكيد الحساب"),
    ("3", "إعداد ملف شخصي"),
    ("4", "بناء سيرتك الذاتية"),
    ("5", "قيد المراجعة"),
    ("6", "مكتمل"),
)

CompanySignupProcessChoices = (
    ("0", "ملغي"),
    ("1", "إنشاء حساب"),
    ("2", "تاكيد الحساب"),
    ("3", "إعداد ملف شخصي"),
    ("4", "قيد المراجعة"),
    ("5", "مكتمل"),
)

SubscriptionsTheemChoices = (
    ('btn btn-primary', 'primary'),
    ('btn btn-secondary', 'secondary'),
    ('btn btn-success', 'success'),
    ('btn btn-danger', 'danger'),
    ('btn btn-warning', 'warning'),
    ('btn btn-info', 'info'),
    ('btn btn-light', 'light'),
    ('btn btn-dark', 'dark'),
)


# Create your models here.
withdraw_status_list = (
    ('0', 'Pending,, قيد الانتظار'),
    ('1', 'Approved,, وافق'),
    ('2', 'Complete,, مكتمل'),
    ('3', 'Cancelled,, ألغيت'),
)
withdrawal_method_list = (
    # ('0','Paypal'),
    # ('1','USDT'),
    ('2','حساب بنكي'),
)
usdt_network_choices = (
    ('0','Tron (TRC20)'),
    ('1','Ethereum (ERC20)'),
    ('2','BNB Smart Chain (BEP20)'),
    ('3','Solana'),
    ('4','Polygon'),
    ('5','Arbitrum One'),
    ('6','Optimism'),
)



def EmployeeRandomNumCodeGen():
    N = 4
    res = ''.join(random.choices(string.digits, k=N))
    return 'i' + str(res)

def CompanyRandomNumCodeGen():
    N = 8
    res = ''.join(random.choices(string.digits, k=N))
    return 'o' + str(res)

def payOrderCodeGen():
    N = 16
    res = ''.join(random.choices(string.digits, k=N))
    return 'o' + str(res)

def WhatsappOTPCodeGen():
    N = 4
    res = ''.join(random.choices(string.digits, k=N))
    return str(res)

def StrNumCodeGen():
    N = 13
    res = ''.join(random.choices(string.digits+ string.ascii_letters, k=N))
    return str(res)
def ResetPWDCodeGen():
    N = 100
    res = ''.join(random.choices(string.digits+ string.ascii_letters, k=N))
    return str(res)

def GenrateRefString(len=6):
    a = ''.join(random.choice(string.ascii_letters) for i in range(len))
    obj = ReferralLinkModel.objects.filter(referral_id=a)
    if obj.exists():
        GenrateRefString(len+1)
    return a



def GenrateUserID(len=6):
    a = ''.join(random.choice(string.digits) for i in range(len))
    obj = User.objects.filter(username=a)
    if obj.exists():
        GenrateUserID(len+1)
    return a

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_employee = models.BooleanField(default=False, null=True, verbose_name="هل هو موظف")
    is_company = models.BooleanField(default=False, null=True, verbose_name="هل هو شركة")

    employeeprofile = models.ForeignKey('EmployeeProfile', on_delete=models.CASCADE, null=True, blank=True)
    companyprofile = models.ForeignKey('CompanyProfile', on_delete=models.CASCADE, null=True, blank=True)

    admin_permission = models.CharField(max_length=255, choices = AdminPermission, null=True, blank=True, verbose_name="الاذونات")
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")

    is_email_verificated = models.BooleanField(default=False, null=True, verbose_name="هل تم تأكيد بريد الالكتروني")
    is_phone_verificated = models.BooleanField(default=False, null=True, verbose_name="هل تم تأكيد الرقم")

    company_signup_process = models.CharField(default='1', max_length=255, choices = CompanySignupProcessChoices, null=True)
    cv_signup_process = models.CharField(default='1', max_length=255, choices = CVSignupProcessChoices, null=True)

    alt_id = models.CharField(max_length=255, default=StrNumCodeGen)

    is_active = models.BooleanField(default=False)
    last_active_datetime = models.DateTimeField(null=True, blank=True)
    
    is_in_chat = models.BooleanField(default=False)
    active_messenger = models.ForeignKey(MessengerModel, on_delete=models.SET_NULL, null=True, blank=True)
    
    subscription = models.ForeignKey('UserSubscriptionModel', on_delete=models.SET_NULL, null=True, blank=True)

    money = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, verbose_name='الرصيد')
    referral = models.ForeignKey('ReferralLinkModel', verbose_name="", on_delete=models.SET_NULL, null=True, blank=True)
    
    dont_receive_msg_from_companys = models.BooleanField(default=False)
    dont_receive_msg_from_employees = models.BooleanField(default=False)
    


    show_phone = models.BooleanField(default=True)
    show_facebook = models.BooleanField(default=True)
    show_linkedin = models.BooleanField(default=True)
    show_whatsapp = models.BooleanField(default=True)
    show_instgram = models.BooleanField(default=True)
    show_snapshat = models.BooleanField(default=True)
    show_tiktok = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    def reminding_subscription_days(self):
        datetime_now = DatetimeNow(self.user)
        date_now = datetime_now.date()
        subscription_date = self.subscription.creation_date.date()
        end_date = (datetime.timedelta(days=self.subscription.number_of_days) + subscription_date)
        reminding_days = (end_date - date_now).days
        if reminding_days <=0:
            reminding_days = 0
        return reminding_days

    def is_has_subscription(self):
        datetime_now = DatetimeNow(self.user)
        date_now = datetime_now.date()
        if self.subscription:
            subscription_date = self.subscription.creation_date.date()
            end_date = (datetime.timedelta(days=self.subscription.number_of_days) + subscription_date)
            if date_now < end_date:
                return True
        
        return False

    def subscription_send_msg_data(self):
        msg_count = self.subscription.number_of_send_msgs
        used_msg_count = self.subscription.used_number_of_send_msgs
        avarible_msg = msg_count - used_msg_count
        is_avarible = True
        if avarible_msg <=0:is_avarible = False
        
        return [is_avarible, avarible_msg, msg_count, used_msg_count]

    def subscription_received_msg_data(self):
        msg_count = self.subscription.number_of_receive_msgs
        used_msg_count = self.subscription.used_number_of_receive_msgs
        avarible_msg = msg_count - used_msg_count
        is_avarible = True
        if avarible_msg <=0:is_avarible = False
        
        return [is_avarible, avarible_msg, msg_count, used_msg_count]


    def subscription_viewed_profile_data(self):
        msg_count = self.subscription.number_of_view_profiles
        used_msg_count = self.subscription.used_number_of_view_profiles
        avarible_msg = msg_count - used_msg_count
        is_avarible = True
        if avarible_msg <=0:is_avarible = False
        
        return [is_avarible, avarible_msg, msg_count, used_msg_count]

class CountrysModel(models.Model):
    name = models.CharField(max_length=255, choices=CountrysChoices, null=True, verbose_name="اسم الدولة")
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")
    def __str__(self):
        return self.get_name_display()
    

class NationalityModel(models.Model):
    name = models.CharField(max_length=255, null=True, verbose_name="الجنسية")
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")
    def __str__(self):
        return self.name

class HealthStatusModel(models.Model):
    name = models.CharField(max_length=255, null=True, verbose_name="الحالة الصحية")
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")
    def __str__(self):
        return self.name


class SkilsModel(models.Model):
    name = models.CharField(max_length=255, null=True, verbose_name="اسم المهارة")
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")
    

    def __str__(self):
        return self.name
    
    
class EmployeeProfile(models.Model):
    name = models.CharField(max_length=250, null=True, verbose_name="الاسم الثلاثي")
    gender = models.CharField(max_length=255, choices = GenderFields, null=True, verbose_name="الجنس")
    age = models.IntegerField(null=True, verbose_name="العمر")
    weight = models.IntegerField(verbose_name="الوزن", null=True)
    height = models.IntegerField(verbose_name="الطول", null=True)
    marital_status = models.CharField(max_length=255, choices = StateFields, null=True, verbose_name="الحالة الإجتماعية")
    health_status = models.ForeignKey(HealthStatusModel, on_delete=models.SET_NULL, null=True, verbose_name='الحالة الصحية')
    phone = models.CharField(max_length=250, null=True, verbose_name="الهاتف")
    phone_country_code = models.CharField(max_length=50, null=True, default='')

    country = models.ForeignKey('CountrysModel', on_delete=models.SET_NULL, null=True, verbose_name='الدولة')
    employee_city = models.CharField(max_length=255, null=True, verbose_name="المدينة")
    district = models.CharField(max_length=250, null=True, verbose_name="الحي")
    nationality = models.ForeignKey('NationalityModel', on_delete=models.SET_NULL, null=True, verbose_name='الجنسية')
    how_hear = models.CharField(max_length=255, choices = HowHearFields, null=True, verbose_name="كيف سمعت عنا")
    how_hear_other = models.CharField(max_length=250, null=True, verbose_name="اذكر لنا كيف سمعت عنا")
    have_car = models.CharField(max_length=255, choices = YesNoFields, null=True, verbose_name="أمتلك سيارة ورخصة قيادة")
    
    about_me = models.TextField(verbose_name='نبذة عني', null=True)
    desires = models.JSONField(verbose_name='الرغبات json', null=True, default=dict)
    experiences = models.JSONField(verbose_name='خبرات json', null=True, default=dict)
    classes = models.JSONField(verbose_name='دورات json', null=True, default=dict)
    skils = models.JSONField(verbose_name='مهارات json', null=True, default=dict)
    lang = models.JSONField(verbose_name='لغات json', null=True, default=dict)



    major = models.CharField(max_length=250, null=True, verbose_name="التخصص الدراسي")
    job_title = models.CharField(max_length=50, null=True, verbose_name="المسمى الوظيفي")
    # skils = models.TextField(verbose_name='المهارات', null=True)

    cert_type = models.CharField(max_length=255, choices = CertTypeFields, null=True, verbose_name="نوع الشهادة")
    learning_domain = models.CharField(max_length=255, choices = LearningDomainFields, null=True, verbose_name="مجال التعلم")

    cv = models.FileField(upload_to="employee_cv/%Y/%m/%d/")
    employee_password = models.CharField(max_length=250, null=True, verbose_name="كلمة المرور للمنصة")
    
    facebook = models.CharField(max_length=250, default='', blank=True, null=True, verbose_name="facebook")
    linkedin = models.CharField(max_length=250, default='', blank=True, null=True, verbose_name="linkedin")
    whatsapp = models.CharField(max_length=250, default='', blank=True, null=True, verbose_name="whatsapp")
    instgram = models.CharField(max_length=250, default='', blank=True, null=True, verbose_name="instgram")
    snapshat = models.CharField(max_length=250, default='', blank=True, null=True, verbose_name="snapshat")
    tiktok = models.CharField(max_length=250, default='', blank=True, null=True, verbose_name="tiktok")

    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")
    def __str__(self):
        return str(self.name)
    

class CompanyProfile(models.Model):
    company_name = models.CharField(max_length=250, null=True, verbose_name="اسم المنشئة")
    complite_name = models.CharField(max_length=250, null=True, verbose_name="اسم مقدم الطلب")
    phone = models.CharField(max_length=250, null=True, verbose_name="الهاتف")
    phone_country_code = models.CharField(max_length=50, null=True, default='')
    about_me = models.TextField(verbose_name='نبذة عني', null=True)
    img_base64 = models.TextField(blank=True, null=True)

    country = models.ForeignKey('CountrysModel', on_delete=models.SET_NULL, null=True, verbose_name='الدولة')
    employee_city = models.CharField(max_length=255, null=True, verbose_name="المدينة")
    district = models.CharField(max_length=250, null=True, verbose_name="الحي")
    
    land_line_number = models.CharField(max_length=250, blank=True, default='', null=True, verbose_name="هاتف ارضي")
    facebook_profile = models.CharField(max_length=250, blank=True, default='', null=True, verbose_name="صفحة فيسبوك")
    linkedin = models.CharField(max_length=250, blank=True, default='', null=True, verbose_name="صفحة لينكداين")
    whatsapp = models.CharField(max_length=250, blank=True, default='', null=True, verbose_name="واتساب")
    instgram = models.CharField(max_length=250, blank=True, default='', null=True, verbose_name="instgram")
    snapshat = models.CharField(max_length=250, blank=True, default='', null=True, verbose_name="snapshat")
    tiktok = models.CharField(max_length=250, blank=True, default='', null=True, verbose_name="tiktok")


    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")
    def __str__(self):
        return str(self.company_name)
    

class EmployeeProfileImages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to="users/profile/imgs/%Y/%m/%d", blank=True, null=True)
    img_base64 = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")



class NotificationsModel(models.Model):
    sender = models.ForeignKey(User, related_name='noti_sender', on_delete=models.CASCADE)
    receiver = models.ManyToManyField(User, related_name='noti_receiver')
    msg = models.TextField()
    is_readed = models.BooleanField(default=False)

    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")

    def whenpublished(self):
        return when_published(self.creation_date)    


class ReferralLinkModel(models.Model):
    alias_name = models.CharField(max_length=250, blank=True, null=True)
    referral_id = models.CharField(default=GenrateRefString, max_length=250, blank=True, null=True)
    creator_userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    total_earn = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, blank=True, null=True)
    withdraw_earn = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, blank=True, null=True)
    all_total_earn = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, blank=True, null=True)
    percentage_of_withdraw = models.IntegerField(blank=True, null=True)
    add_balance_for_signup = models.BooleanField(default=False, verbose_name="اضافة رصيد للمنشاء الحساب")
    add_balance_for_signup_amount = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, verbose_name="كمية اضافة رصيد للمنشاء الحساب", blank=True, null=True)
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")

    def __str__(self):
        return self.referral_id
    
    def get_absolute_url(self):

        return reverse("SignUpReferralLink", args=[str(self.referral_id)])


class ViewersCounterByIPADDR(models.Model):
    ip_addr = models.CharField(max_length=255)
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")


class SubscriptionsModel(models.Model):
    title = models.CharField(max_length=255, verbose_name='العنوان')
    subtitle = models.CharField(max_length=255, verbose_name='العنوان الفرعي')
    ico = models.TextField(verbose_name='الأيقونة')

    Theem = models.CharField(max_length=255, choices=SubscriptionsTheemChoices, null=True, verbose_name='الثيم')

    is_default_Subscription = models.BooleanField(default=False, verbose_name='هل هذه الباقة الافتراضية عند التسجيل')

    number_of_days = models.IntegerField(default=30, verbose_name='عدد الأيام')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='السعر')
    currency = models.CharField(max_length=250, choices=CurrencyChoices, default='USD', null=True, verbose_name='العملة')

    number_of_receive_msgs = models.IntegerField(default=1, verbose_name='عدد الرسائل المستلمة')
    number_of_send_msgs = models.IntegerField(default=1, verbose_name='عدد الرسائل المرسلة')
    number_of_view_profiles = models.IntegerField(default=1, verbose_name='عدد مرات مشاهدة الملفات الشخصية')

    show_phone = models.BooleanField(default=False, verbose_name='إظهار رقم الهاتف')
    show_whats = models.BooleanField(default=False, verbose_name='إظهار رقم الواتساب')
    show_facebook = models.BooleanField(default=False, verbose_name='إظهار الفيسبوك')
    show_linkedin = models.BooleanField(default=False, verbose_name='إظهار لينكدإن')
    show_instgram = models.BooleanField(default=False, verbose_name='إظهار الإنستغرام')
    show_snap = models.BooleanField(default=False, verbose_name='إظهار السناب شات')
    show_tiktok = models.BooleanField(default=False, verbose_name='إظهار التيك توك')
    show_userprofile_img = models.BooleanField(default=False, verbose_name='إظهار صورة الملف الشخصي')

    distinctive_mark = models.BooleanField(default=False, verbose_name='علامة مميزة')
    distinctive_frame = models.BooleanField(default=False, verbose_name='إطار مميز')

    show_number_of_appearances = models.BooleanField(default=False, verbose_name='إظهار عدد الظهور')
    show_number_of_likes = models.BooleanField(default=False, verbose_name='إظهار عدد الإعجابات')
    referral_link_to_earn = models.BooleanField(default=False, verbose_name='رابط الإحالة للربح')

    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")

    def __str__(self):
        return str(self.title)
    

class UserSubscriptionModel(models.Model):
    subscription = models.ForeignKey('SubscriptionsModel', on_delete=models.CASCADE)
    number_of_days = models.IntegerField(default=30)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    number_of_receive_msgs = models.IntegerField(default=1)
    used_number_of_receive_msgs = models.IntegerField(default=0)
    number_of_send_msgs = models.IntegerField(default=1)
    used_number_of_send_msgs = models.IntegerField(default=0)
    number_of_view_profiles = models.IntegerField(default=1)
    used_number_of_view_profiles = models.IntegerField(default=0)
    creation_date = models.DateTimeField(null=True, default=timezone.now, verbose_name="تاريخ الانشاء")
    def __str__(self):
        return str(self.subscription.title)


class UserViewedProfileModel(models.Model):
    profile_viewer = models.ForeignKey(User, related_name='profile_viewer', on_delete=models.CASCADE)
    profile_viewed = models.ForeignKey(User, related_name='profile_viewed', on_delete=models.CASCADE)
    ignore_subscription = models.BooleanField(default=False)
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")

class UserPaymentOrderModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    subscription = models.ForeignKey(SubscriptionsModel, on_delete=models.SET_NULL, null=True)
    orderID = models.CharField(max_length=250, default=payOrderCodeGen, null=True, verbose_name="الاسم الثلاثي")
    transactionNo = models.CharField(max_length=250, null=True)
    is_buyed = models.BooleanField(default=False)
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")



class WhatsappOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    secret = models.CharField(max_length=250, default=WhatsappOTPCodeGen, null=True)

    phone = models.CharField(max_length=250, blank=True, null=True)
    country_code = models.CharField(max_length=250, blank=True, null=True)
    
    is_finshed = models.BooleanField(default=False)

    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")

class EmailOTPModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    secret = models.CharField(max_length=250, default=WhatsappOTPCodeGen, null=True)
    is_finshed = models.BooleanField(default=False)

    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")


class UserLikeModel(models.Model):
    liker = models.ForeignKey(User, related_name='liker', on_delete=models.SET_NULL, null=True)
    liked = models.ForeignKey(User, related_name='liked', on_delete=models.SET_NULL, null=True)
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")




class SubscriptionPriceByCountry(models.Model):
    subscription = models.ForeignKey(SubscriptionsModel, on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey('CountrysModel', on_delete=models.SET_NULL, null=True, verbose_name='الدولة')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    currency = models.CharField(max_length=250, choices=CurrencyChoices, null=True)

    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")


class AdminADSModel(models.Model):
    img = models.ImageField(upload_to='ADS/%Y/%m/')
    redirect_url = models.CharField(max_length=254)
    country = models.ForeignKey('CountrysModel', on_delete=models.SET_NULL, null=True, verbose_name='الدولة')
    available_num_of_days = models.IntegerField()
    is_main_ad = models.BooleanField(default=False, verbose_name='انه اعلان الرئيسي')
    show_in_cv = models.BooleanField(default=False, verbose_name='اظهار بين السير')
    show_in_others = models.BooleanField(default=False, verbose_name='اظهار بين الاقسام الاخرى للموقع')
    show_on_all_countrys = models.BooleanField(default=False, verbose_name='عرض في جميع الدول')
    is_enabled = models.BooleanField(default=True)
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")

    def reminding_days(self):
        datetime_now = DatetimeNow(None)
        date_now = datetime_now.date()
        subscription_date = self.creation_date.date()
        end_date = (datetime.timedelta(days=self.available_num_of_days) + subscription_date)
        reminding_days = (end_date - date_now).days
        if reminding_days <=0:
            reminding_days = 0
        return reminding_days
    

class ForgetPWDModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    secret = models.CharField(max_length=250, default=ResetPWDCodeGen, null=True)
    is_finshed = models.BooleanField(default=False)

    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")


class AdminPermissionModel(models.Model):
    is_enabled = models.BooleanField(default=True, verbose_name='هل المسؤول مفعل')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='المستخدم')

    show_employees = models.BooleanField(default=False, verbose_name='عرض الموظفين')
    delete_employees = models.BooleanField(default=False, verbose_name='حذف الموظفين')
    edit_employees = models.BooleanField(default=False, verbose_name='تعديل_الموظفين')

    show_companys = models.BooleanField(default=False, verbose_name='عرض الشركات')
    delete_companys = models.BooleanField(default=False, verbose_name='حذف_الشركات')
    edit_companys = models.BooleanField(default=False, verbose_name='تعديل_الشركات')

    show_jobs = models.BooleanField(default=False, verbose_name='عرض الوظائف')
    delete_jobs = models.BooleanField(default=False, verbose_name='حذف الوظائف')
    edit_jobs = models.BooleanField(default=False, verbose_name='تعديل الوظائف')

    show_subscription = models.BooleanField(default=False, verbose_name='عرض الاشتراك')
    add_subscription = models.BooleanField(default=False, verbose_name='إضافة_اشتراك')
    delete_subscription = models.BooleanField(default=False, verbose_name='حذف_الاشتراك')
    edit_subscription = models.BooleanField(default=False, verbose_name='تعديل الاشتراك')

    show_custum_subscription = models.BooleanField(default=False, verbose_name='عرض الاشتراك المخصص')
    add_custum_subscription = models.BooleanField(default=False, verbose_name='إضافة اشتراك مخصص')
    delete_custum_subscription = models.BooleanField(default=False, verbose_name='حذف_الاشتراك_المخصص')
    edit_custum_subscription = models.BooleanField(default=False, verbose_name='تعديل_الاشتراك_المخصص')

    show_ads = models.BooleanField(default=False, verbose_name='عرض الإعلانات')
    add_ads = models.BooleanField(default=False, verbose_name='إضافة إعلانات')
    delete_ads = models.BooleanField(default=False, verbose_name='حذف_الإعلانات')
    edit_ads = models.BooleanField(default=False, verbose_name='تعديل_الإعلانات')

    show_countrys = models.BooleanField(default=False, verbose_name='إظهار البلدان')
    add_countrys = models.BooleanField(default=False, verbose_name='إضافة البلدان')
    delete_countrys = models.BooleanField(default=False, verbose_name='حذف_البلدان')
    edit_countrys = models.BooleanField(default=False, verbose_name='تعديل_البلدان')

    show_nationality = models.BooleanField(default=False, verbose_name='إظهار_الجنسية')
    add_nationality = models.BooleanField(default=False, verbose_name='إضافة_جنسية')
    delete_nationality = models.BooleanField(default=False, verbose_name='حذف_الجنسية')
    edit_nationality = models.BooleanField(default=False, verbose_name='تعديل_الجنسية')

    send_notifications = models.BooleanField(default=False, verbose_name='إرسال الإشعارات')

    edit_settings = models.BooleanField(default=False, verbose_name='تعديل الإعدادات')

    show_user_subscription = models.BooleanField(default=False, verbose_name='إظهار اشتراك المستخدم')
    edit_user_subscription = models.BooleanField(default=False, verbose_name='تعديل اشتراك المستخدم')




class Withdraw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='المستخدم')
    status = models.CharField(choices=withdraw_status_list, max_length=250, verbose_name="الحالة")
    total_amount = models.DecimalField(max_digits=6, decimal_places=3, verbose_name='كمية السحب')
    withdrawal_method = models.CharField(choices=withdrawal_method_list, max_length=250, verbose_name="نوع السحب")

    usdt_network = models.CharField(choices=usdt_network_choices, max_length=250, verbose_name="شبكة usdt", blank=True, null=True)
    usdt_address = models.CharField(max_length=250, verbose_name="عنوان محفظة usdt", blank=True, null=True)


    full_name = models.CharField(max_length=250, verbose_name="عنوان محفظة usdt", blank=True, null=True)
    bank_name = models.CharField(max_length=250, verbose_name="عنوان محفظة usdt", blank=True, null=True)
    bank_account_number = models.CharField(max_length=250, verbose_name="عنوان محفظة usdt", blank=True, null=True)
    IBAN_number = models.CharField(max_length=250, verbose_name="عنوان محفظة usdt", blank=True, null=True)

    desc = models.TextField(verbose_name='وصف')
    is_completed = models.BooleanField(default=False, verbose_name='دفعت')
    withdraw_date = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ السحب')


    class Meta:
        ordering = ['-withdraw_date']

    def __str__(self):
        return self.user.username

    def get_status_ar(self):
        for i in withdraw_status_list:
            if i[0] == self.status:
                return i[1].split(',,')[1]

    def get_status_en(self):
        for i in withdraw_status_list:
            if i[0] == self.status:
                return i[1].split(',,')[0]

    def get_withdrawal_method(self):
        for i in withdrawal_method_list:
            if i[0] == self.withdrawal_method:
                return i[1]