from django.db import models
from django.contrib.auth.models import User
import string
import random
from django.utils import timezone
import math

# Create your models here.


def RandomRoomIDGen():
    N = 25
    res = ''.join(random.choices(string.digits, k=N))
    return 'i' + str(res)


class MessengerModel(models.Model):
    messenger_users = models.ManyToManyField(User)

    room_id = models.CharField(max_length=255, default=RandomRoomIDGen)

    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")

class MessagesModel(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    msg = models.TextField()

    messenger = models.ForeignKey(MessengerModel, on_delete=models.CASCADE)

    is_readed = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="تاريخ الانشاء")



    def whenpublished(self):
        now = timezone.now()
        
        diff= now - self.creation_date

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) + " ثانية"
            
            else:
                return str(seconds) + " ثواني"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes)  + " دقيقة"
            
            else:
                return str(minutes)  + " دقيقة"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " ساعة"

            else:
                return str(hours) + " ساعات"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " يوم"

            else:
                return str(days) + " ايام"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " شهر"

            else:
                return str(months) + " اشهر"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " سنة"

            else:
                return str(years) + " سنوات"

