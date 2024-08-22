import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import MessagesModel, MessengerModel, BlockUserModel
from accounts.models import UserProfile, UserSubscriptionModel, CompanyRandomNumCodeGen
from django.contrib.auth.models import User
from channels.layers import get_channel_layer

class chatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.msg_model = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        user = self.scope["user"]
        userprofile = UserProfile.objects.get(id=user.userprofile.id)
        userprofile.is_in_chat = True
        userprofile.active_messenger = MessengerModel.objects.get(room_id=self.room_name)
        userprofile.save()

        # connection has to be accepted
        self.accept()

        # join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        room = MessengerModel.objects.get(room_id=self.room_name)
        msgs_model = MessagesModel.objects.filter(messenger=room, is_readed=False)
        for i in msgs_model.exclude(sender=user):
            i.is_readed = True
            i.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'msg_read_all',
                'method':'msg_read_all',
                'user_id': user.id,
            }
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

        user = self.scope["user"]
        userprofile = UserProfile.objects.get(id=user.userprofile.id)
        userprofile.is_in_chat = False
        userprofile.save()

    def receive(self, text_data=None, bytes_data=None):


        text_data_json = json.loads(text_data)
        method = text_data_json['method']
        user = self.scope["user"]
        userprofile = UserProfile.objects.get(user=user)
        room = MessengerModel.objects.get(room_id=self.room_name)
        sender_subscription_end_msg = 'نفذ عدد ارسال الرسائل يرجى ترقية او تجديد العضوية لارسال الرسالة'
        receiver_subscription_end_msg = 'نفذ عدد استقبال الرسائل يرجى ترقية او تجديد العضوية لاظهار الرسالة'
        # send chat message event to the room

        if method == 'send_msg':
            receiver = room.messenger_users.exclude(id=user.id).first()
            receiver_profile = UserProfile.objects.get(user=receiver)

            is_blocked = BlockUserModel.objects.filter(creator=receiver, user=user).exists()
            his_blocked = BlockUserModel.objects.filter(creator=user, user=receiver).exists()
            is_disable_receive_msg = False

            if userprofile.is_employee:
                if receiver_profile.dont_receive_msg_from_employees:
                    is_disable_receive_msg = True

            if userprofile.is_company:
                if receiver_profile.dont_receive_msg_from_companys:
                    is_disable_receive_msg = True
                    

            sender_subscription_passed = False
            receiver_subscription_passed = False
            if userprofile.subscription:
                if userprofile.subscription_send_msg_data()[0]:
                    user_sub = UserSubscriptionModel.objects.get(id=userprofile.subscription.id)
                    user_sub.used_number_of_send_msgs += 1
                    user_sub.save()
                    sender_subscription_passed = True
            else:
                sender_subscription_end_msg = 'يرجى الاشتراك في باقة لتتمكن من ارسال الرسائل'
            if userprofile.subscription:
                    
                if receiver_profile.subscription_received_msg_data()[0]:
                    receiver_subscription_passed = True
                    receiver_sub = UserSubscriptionModel.objects.get(id=receiver_profile.subscription.id)
                    receiver_sub.used_number_of_receive_msgs += 1
                    receiver_sub.save()

            if is_blocked or his_blocked or is_disable_receive_msg:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'method':'Blocked',
                    }
                )
            elif not sender_subscription_passed:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'method':'subscription',
                        'user_id': user.id,
                        'sender_subscription_passed':sender_subscription_passed,
                        'msg':sender_subscription_end_msg,
                        'toastID': CompanyRandomNumCodeGen(),
                    }
                )
            else:

                message = text_data_json['message']
                msg_model = MessagesModel.objects.create(msg=message, messenger=room, sender=user)

                send_toast = False
                is_active = receiver.userprofile.is_active
                if is_active:
                    if receiver.userprofile.is_in_chat and receiver.userprofile.active_messenger!=room:
                        send_toast = True
                    elif not receiver.userprofile.is_in_chat:
                        send_toast = True

                msg_model.is_receiver_subscription_passed = receiver_subscription_passed
                msg_model.save()
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'method':method,
                        'user_id': user.id,
                        'receiver_id': receiver.id,
                        'msg_id': msg_model.id,
                        'message': message,
                        'send_toast':send_toast,
                        'is_active':is_active,
                        'sender_subscription_passed':sender_subscription_passed,
                        'receiver_subscription_passed':receiver_subscription_passed,
                        'receiver_subscription_end_msg':  receiver_subscription_end_msg,
                        'creation_date': msg_model.creation_date.strftime('%H:%M'),
                    }
                )

        elif method == 'msg_readed':
            msg_id = text_data_json['msg_id']
            msg_model = MessagesModel.objects.get(id=msg_id)
            msg_model.is_readed = True
            msg_model.save()
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'msg_readed',
                    'method':method,
                    'user_id': user.id,
                    'msg_id': msg_id,
                }
            )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def msg_readed(self, event):
        self.send(text_data=json.dumps(event))

    def msg_read_all(self, event):
        self.send(text_data=json.dumps(event))

    def showToast(self, event):
        self.send(text_data=json.dumps(event))

# code src = https://testdriven.io/blog/django-channels/, https://www.youtube.com/watch?v=cw8-KFVXpTE

