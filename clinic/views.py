from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view , schema
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status

import urllib
import datetime
from clinic.models import pp_clinic_master
from clinic.serializers import pp_clinic_masterSerializer
import json
import random



def get_ip(request):
    try:
        x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward:
            ip = x_forward.split(",")[0]
        else:
            ip =request.META.get("REMOTE_ADDR")    
    except:
        ip = ' '
    return ip            




@csrf_exempt
@api_view(['POST'])
def add_clinic(request):

    data = request.data
    list1 = [1, 2, 3, 4, 5, 6,7,8,9,0]
    data['last_update_by'] = get_ip(request)
    serializer = pp_clinic_masterSerializer(data = data)
    if serializer.is_valid():
        code = serializer.save()
        code.clinic_code = 'C' + str(random.choice(list1)) + str(code.pp_cm_id)
        code.save()
        
        return Response({"message":"clinic added"},status = status.HTTP_201_CREATED)
    return Response(serializer.errors)    



@csrf_exempt
@api_view(['GET'])
def get_clinic(request):
    data = pp_clinic_master.objects.all()
    seializer = pp_clinic_masterSerializer(data,many = True)
    return Response(seializer.data)
