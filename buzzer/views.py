import random
import string
import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.core.mail import send_mail

from core.settings import ACTIVE_ROOMS
# Create your views here.

def send_mail_view(request, *args, **kwargs):
    if request.method == 'POST':
        
        if request.POST.get('info') == "sendmail":
            print(request.POST.get("mailbody"))
            rawMailBody = json.loads(request.POST.get('mailbody'))
            mailBody=""
            for key, value in rawMailBody.items():
                mailBody += "<br>"+value
            body = 'Hello There, <br><br>Fun Friday Game Scores: <br>'+ mailBody +'<br><br><br>Regards<br>ESC Software Incubation Team<br>'
            recipient = request.POST.get('sendto')
            if "@easymail.example.com" in recipient:
                body = '<!DOCTYPE html><html><body>'+body+'</body></html>'
            else:
                body = body.replace("<br>","\n")
            send_mail(
            'From Buzzer App',
            body,
            'example@example.com',
            recipient_list=[recipient], 
            # recipient_list=["avinash1.kumar@orange.com"],
            fail_silently=False,
            )
            print("Mail sent successfully!!")
        context = {
            "info": "success",
        }
        return JsonResponse(context)

def index(request, *args, **kwargs):
    if request.method == 'POST':
    
        username = request.POST.get('username')
        room_code = request.POST.get('room_code')
        # request.session['room_code'] = room_code
        # request.session['room_username'] = username
        return redirect("/player/"+room_code +"/"+username)
        
    context = {}
    return render(request, 'buzzer/index.html')
# active_rooms =[]

def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))

def host(request, *args, **kwargs):
    room_code = ""
    room_name = "host"
    request.session['room_name'] = room_name
    
    # print(ACTIVE_ROOMS, request.session['room_code'])

    if 'room_code' in request.session and request.session['room_code'] not in ACTIVE_ROOMS:
        room_code = request.session['room_code']
        ACTIVE_ROOMS.append(room_code)
    else:
        room_code = generate_room_code()
        while room_code in ACTIVE_ROOMS:
            room_code = generate_room_code()
        request.session['room_code'] = room_code
        ACTIVE_ROOMS.append(room_code)
        # print(ACTIVE_ROOMS)
    
    context = {
        "room_code": room_code,
    }
    return render(request, 'buzzer/host.html', context)

def players(request, *args, **kwargs):
    # if 'room_code' in request.session:
    #     room_code = request.session['room_code']

    if request.method == 'POST':
    
        username = request.POST.get('username')
        room_code = request.POST.get('room_code')
        request.session['room_code'] = room_code
        request.session['room_username'] = username
    else:
        return redirect("/")
    context = {
        'username': username,
        'room_code': room_code,
    }
    return render(request, 'buzzer/players.html', context)

