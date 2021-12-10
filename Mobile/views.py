from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view , schema
from exercise.models import ex_exercise_master ,ex_joint_master,ex_movement_master,ex_muscles_master,ex_excercise_joints_mapping,ex_excercise_movement_mapping,ex_excercise_muscle_mapping,ex_care_plan
from exercise.serializer import ex_exercise_master_masterSerializer,ex_joint_masterSerializer,ex_movement_masterSerializer,ex_muscles_masterSerializer,ex_excercise_joints_mappingSerializer,ex_excercise_muscle_mappingSerializer,ex_excercise_movement_mappingSerializer,ex_care_planSerializer
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status
import jwt , datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from patient.models import pp_patient_master
from patient.serializer import pp_patient_master_masterSerializer
import random












@csrf_exempt
@api_view(['GET'])
def get_care_plan(request):

    try:
        id = request.GET.get("id")
        date = request.GET.get("date")
        data = ex_care_plan.objects.filter(episode_id = id,date=date)
        data = ex_care_planSerializer(data,many = True)
#        print(data.data)
        exercise_data = ex_exercise_master.objects.filter(ex_em_id = data.data[0]['exercise_details'][0]['ex_em_id'])
        exercise_serializer = ex_exercise_master_masterSerializer(exercise_data,many = True)
        data.data[0]['exercises'] = exercise_serializer.data[0]['title']
        data.data[0]['exercise_status'] = data.data[0]['time_slot']
        if type(data.data[0]['time_slot']) == dict:
            data.data[0]['time_slot'] = list(data.data[0]['time_slot'].keys())
        return Response(data.data)
    except:
        return Response(status = status.HTTP_400_BAD_REQUEST)



    

@csrf_exempt 
@api_view(['GET'])
def patient_profile(request,id = None):
    try:
       
        profile = pp_patient_master.objects.filter(pp_patm_id = id).first()
        serializer = pp_patient_master_masterSerializer(profile)
        return Response(serializer.data)
    except:
        return  Response(status = status.HTTP_400_BAD_REQUEST)   










# Create your views here.
