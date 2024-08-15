from django.shortcuts import render
from .models import MessagesModel, MessengerModel
from accounts.models import EmployeeProfileImages
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