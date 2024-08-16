from django.shortcuts import render, redirect
from .models import MessagesModel, MessengerModel
from accounts.models import EmployeeProfileImages
from django.contrib.auth.models import User
from django.db.models import Q
# Create your views here.

def get_user_img(user):
    employee_images = EmployeeProfileImages.objects.filter(user=user)
    employee_image = ''
    if employee_images.exists():
        employee_image = employee_images.first().img_base64

    img = []
    if user.userprofile.is_employee:
        if employee_image:
            img = [employee_image, 0]
        else:
            img = ['', 1]
    elif user.userprofile.is_company:
        if user.userprofile.companyprofile.img_base64:
            img = [user.userprofile.companyprofile.img_base64, 0]
        else:
            img = ['', 1]
    else:
        img = ['', 1]
    return img

def messageRoom(request, room_id):
    messenger = MessengerModel.objects.get(room_id=room_id)
    
    receiver = messenger.messenger_users.exclude(id=request.user.id).first()
    
    messages_list = []
    last_date = None
    msg_date = []
    messages = MessagesModel.objects.filter(messenger__room_id=room_id)
    for msg in messages:
        if last_date == None:
            
            last_date=msg.creation_date.date()
        elif msg.creation_date.date() != last_date:
            
            messages_list.append([last_date, msg_date])
            last_date=msg.creation_date.date()
            msg_date = []
            
        msg_date.append(msg)
    messages_list.append([last_date, msg_date])


    profile_image = get_user_img(receiver)
    return render(request, 'messenger/viewMessage.html', {'messages_list':messages_list, 'room_id':room_id, 'receiver':receiver, 'profile_image':profile_image})


def get_messenger_model(sender, receiver):
    messengers = MessengerModel.objects.filter(messenger_users=sender).filter(messenger_users=receiver)
    return messengers

def createMessager(request, receiver_id):
    sender = request.user
    receiver = User.objects.get(id=receiver_id)
    
    messengers = get_messenger_model(sender, receiver)

    if sender != receiver:
        room_id = None
        if not messengers.exists():    
            messenger = MessengerModel.objects.create()
            messenger.messenger_users.set([sender, receiver])
            messenger.save()
            room_id = messenger.room_id
        else:
            room_id = messengers.first().room_id
        return redirect('messageRoom', room_id)
    else:
        return redirect('index')