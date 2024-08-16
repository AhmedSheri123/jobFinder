import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.utils import timezone


class chatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.msg_model = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'{self.room_name}'
        user = self.scope["user"]

        # connection has to be accepted
        self.accept()
        
        # join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

        print(self.channel_name)

        userprofile = UserProfile.objects.get(id=user.userprofile.id)
        userprofile.is_active = True
        userprofile.save()
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
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
        userprofile.is_active = True
        userprofile.last_active_datetime = timezone.now()
        userprofile.save()

    def receive(self, text_data=None, bytes_data=None):
        print('----------------------------->>')
        text_data_json = json.loads(text_data)
        method = text_data_json['method']
        user = self.scope["user"]
        

        # send chat message event to the room

        if method == 'showToast':
            message = text_data_json['message']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'showToast',
                    'method':method,
                    'receiver_id': user.id,
                    'message': message,
                }
            )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))



# code src = https://testdriven.io/blog/django-channels/, https://www.youtube.com/watch?v=cw8-KFVXpTE
