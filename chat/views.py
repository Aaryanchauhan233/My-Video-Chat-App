from django.shortcuts import render
from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
import random
import time
import json

from .models import RoomMember
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def getToken(request):
    appId = '761b563f15844bebbce1fd19210bad42'
    appCertificate = 'd7c0ef7b15be4b2ea90285dd074ac208'
    channelName = request.GET.get('channel')
    uid = random.randint(1,2890)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp +  expirationTimeInSeconds
    role = 1
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token, 'uid':uid},safe=False)


def home(request):
    return render(request, 'chat/home.html')


def room(request):
    return render(request, 'chat/room.html')

@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    
    member, created = RoomMember.objects.get_or_create(
        name = data['name'],
        uid = data['UID'],
        room_name = data['room_name']
    )
    return JsonResponse({'name':data['name']}, safe=False)

def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')
    
    try:
        member = RoomMember.objects.get(uid=uid, room_name=room_name)
        name = member.name
        return JsonResponse({'name': name}, safe=False)
    except RoomMember.DoesNotExist:
        return JsonResponse({'error': 'Member does not exist'}, status=404)
    

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    
    member = RoomMember.objects.get(
        name = data['name'],
        uid = data['UID'],
        room_name = data['room_name'],
    )
    member.delete()
    return JsonResponse('Member was deleted!!!', safe=False)