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

import random



@csrf_exempt
@api_view(['GET','POST'])
def get_exercise(request,page = None):

    data  = ex_exercise_master.objects.all()
    count = data.count()
    paginator = Paginator(data,request.data['page_size'])
    page = request.data['page_no']
    try:
        serializer = ex_exercise_master_masterSerializer(paginator.page(page),many =True)
      
        for i in range(0,len(serializer.data)):
            serializer.data[i]['joint'] = []
            try:
                angle = ex_excercise_joints_mapping.objects.filter(ex_em_id = serializer.data[i]['ex_em_id']).order_by('-joint_priority')
                angle = ex_excercise_joints_mappingSerializer(angle,many = True)
                serializer.data[i]['angle'] = {}


                for j in range(0,len(angle.data)):
                   # {"max_angle":angle.data[0]['max_angle'],"min_angle":angle.data[0]['min_angle']}
                
                    joint = ex_joint_master.objects.filter(ex_jm_id = angle.data[j]['ex_jm_id'])
                    joint = ex_joint_masterSerializer(joint,many = True)
                    serializer.data[i]['angle'][joint.data[0]['joint_name']] = {}
                    serializer.data[i]['angle'][joint.data[0]['joint_name']]['min'] = angle.data[j]['min_angle']
                    serializer.data[i]['angle'][joint.data[0]['joint_name']]['max'] = angle.data[j]['max_angle']

                serializer.data[i]['joint'] = []
                for z in range(0,len(angle.data)):
                    temp = ex_joint_master.objects.filter(ex_jm_id = angle.data[z]['ex_jm_id']).first()
                    temp = ex_joint_masterSerializer(temp)
                    serializer.data[i]['joint'].append(temp.data['joint_name'])
            except:
                pass
	        	

        if int(request.data['page_no']) == 1: 
            return Response({"data":serializer.data,"total_exercise":count})
        else:
            return Response({"data":serializer.data})


    except EmptyPage:
        return Response({"message":"no more pages available"})    


 
@csrf_exempt
@api_view(['POST'])
def search_exercise(request):
   # print(request.data['testing'])
    # if 'joints' in request.data:    
    #     q1 = ex_joint_master.objects.filter(joint_name = request.data['joints'])
    #     count = q1.count()
    #     serializer = ex_joint_masterSerializer(q1,many = True)
    #     pk = serializer.data[0]['ex_jm_id']

    #     q2 = ex_excercise_joints_mapping.objects.filter(ex_jm_id = pk)
    #     serializer = ex_excercise_joints_mappingSerializer(q2,many = True)
    #     count = q2.count()
    #     pk =[] 
    #     for i in range(count):
    #         pk.append(serializer.data[i]["ex_em_id"])

    #     q3 = ex_exercise_master.objects.filter(pk__in = pk)
    #     serializer = ex_exercise_master_masterSerializer(q3,many = True)    

    #     return Response(serializer.data)
    final_q = None
    if 'muscles' in request.data:    
        q1 = ex_muscles_master.objects.filter(muscle_name__in = request.data['muscles'])
        count = q1.count()
        serializer = ex_muscles_masterSerializer(q1,many = True)
        pk =[]
        for i in range(count):
            pk.append(serializer.data[i]['ex_mus_id'])

        q2 = ex_excercise_muscle_mapping.objects.filter(ex_mus_id__in = pk)
        serializer = ex_excercise_muscle_mappingSerializer(q2,many = True)
        count = q2.count()
        pk = []
        for i in range(count):
            pk.append(serializer.data[i]["ex_em_id"])

        q_muscle = ex_exercise_master.objects.filter(pk__in = pk)
        serializer = ex_exercise_master_masterSerializer(q_muscle,many = True)    
        if final_q is None:
            final_q = q_muscle
        else:    
            final_q = final_q | q_muscle
       # return Response(serializer.data)


    if 'movement' in request.data:    
        q1 = ex_movement_master.objects.filter(moment_direction__in = request.data['movement'])
        count = q1.count()
        serializer = ex_movement_masterSerializer(q1,many = True)
        pk =[]
        for i in range(count):
            pk.append(serializer.data[i]['ex_mov_id'])

        q2 = ex_excercise_movement_mapping.objects.filter(ex_mov_id__in = pk)
        serializer = ex_excercise_movement_mappingSerializer(q2,many = True)
        count = q2.count()
        pk =[] 
        for i in range(count):
            pk.append(serializer.data[i]["ex_em_id"])

        q5 = ex_exercise_master.objects.filter(pk__in = pk)
        serializer = ex_exercise_master_masterSerializer(q5,many = True)    
        if final_q is None:
            final_q = q5
        else:    
            final_q = final_q | q5
       # return Response(serializer.data)


    if "difficulty_level" in request.data:

        data = ex_exercise_master.objects.filter(difficulty_level__in = request.data['difficulty_level'])
        serializer = ex_exercise_master_masterSerializer(data,many = True)
        if final_q is None:
            final_q = data
        else:
            final_q = final_q | data    
        #return Response(serializer.data)    
    
    if 'joints' in request.data:    
        q1 = ex_joint_master.objects.filter(joint_name__in = request.data['joints'])
        count = q1.count()
        serializer = ex_joint_masterSerializer(q1,many = True)
        pk = []
 #       print(serializer.data)
        for i in range(count):
            pk.append(serializer.data[i]['ex_jm_id'])
#            print(serializer.data[i]['ex_jm_id'])

        q2 = ex_excercise_joints_mapping.objects.filter(ex_jm_id__in = pk)
        serializer = ex_excercise_joints_mappingSerializer(q2,many = True)
        count = q2.count()
        pk =[] 
        for i in range(count):
            pk.append(serializer.data[i]["ex_em_id"])

        q3 = ex_exercise_master.objects.filter(pk__in = pk)
        serializer = ex_exercise_master_masterSerializer(q3,many = True)    
        if final_q is None:
            final_q = q3
        else:    
            final_q = final_q | q3
         



   
    if final_q is None:
        return Response(status = status.HTTP_400_BAD_REQUEST)

    count = final_q.count()
  
    paginator = Paginator(final_q,request.data['page_size'])
    page = request.data['page_no']
    try:
        serializer = ex_exercise_master_masterSerializer(paginator.page(page),many = True)

        
        for i in range(0,len(serializer.data)):
            try:
                serializer.data[i]['primary_angles'] = []
                angle = ex_excercise_joints_mapping.objects.filter(ex_em_id = serializer.data[i]['ex_em_id'])
                angle = ex_excercise_joints_mappingSerializer(angle,many = True)
                serializer.data[i]['angle'] = {"max_angle":angle.data[0]['max_angle'],"min_angle":angle.data[0]['min_angle']}
            
                joint = ex_joint_master.objects.filter(ex_jm_id = angle.data[0]['ex_jm_id'])
                joint = ex_joint_masterSerializer(joint,many = True)

                serializer.data[i]['joint'] = joint.data[0]['joint_name']
                for z in range(0,len(angle.data)):
                    temp = ex_joint_master.objects.filter(ex_jm_id = angle.data[z]['ex_jm_id']).first()
                    temp = ex_joint_masterSerializer(temp)
                    serializer.data[i]['primary_angles'].append(temp.data['joint_name'])
               
            except:
                pass
    

        if int(request.data['page_no']) == 1:
            return Response({'data':serializer.data,"total_exercise with applied filter":count})
        else:
         

            return Response({'data':serializer.data})  

    except EmptyPage:
        return Response({'message':"no more pages available"})
     



@csrf_exempt
@api_view(['POST'])
def exercise_base_on_joints(request):
    try:
        data = ex_exercise_master.objects.filter(title__in = request.data['exercise'])
        serializer = ex_exercise_master_masterSerializer(data,many = True)
        pk = []
        for i in range(data.count()):
            pk.append(serializer.data[i]['ex_em_id'])

        q2 = ex_excercise_joints_mapping.objects.filter(ex_em_id__in = pk)
        serializer = ex_excercise_joints_mappingSerializer(q2,many = True)    


        count = q2.count()
        pk =[] 
        for i in range(count):
            pk.append(serializer.data[i]["ex_jm_id"])

        q3 = ex_joint_master.objects.filter(pk__in = pk)
        serializer = ex_joint_masterSerializer(q3,many = True) 

  #      print(serializer.data[0])
      #  serializer.data['satwik'] = 'none'
        return Response(serializer.data)

    except:
        return Response(status = status.HTTP_400_BAD_REQUEST)    




import pandas as pd
from datetime import date, timedelta
@csrf_exempt
@api_view(['POST'])
def add_care_plan(request):
    list1 = [1, 2, 3, 4, 5, 6,7,8,9,0]
    request.data['careplan_code'] = 'cp'+ str(random.choice(list1))+str(random.choice(list1)) 
    sdate = date(int(request.data['startDate'][0:4]), int(request.data['startDate'][-5:-3]), int(request.data['startDate'][-2:]))
    edate = date(int(request.data['endDate'][0:4]), int(request.data['endDate'][-5:-3]), int(request.data['endDate'][-2:]))
    index = [sdate+timedelta(days=x) for x in range((edate-sdate).days+1)]
    start_date = request.data['startDate']
    end_date = request.data['endDate']
    temp = []
    for i in range(0,len(request.data['timeSlots'])):
        temp.append([request.data['timeSlots'][i],"planned"])
    temp = {}
    output_json = {}
    for i in range(0,len(request.data['timeSlots'])):
        temp[request.data['timeSlots'][i]] = {}
        output_json[request.data['timeSlots'][i]] = {}
        for j in range(0,len(request.data['exercise_details'])):
            temp[request.data['timeSlots'][i]][request.data['exercise_details'][j]['name']] = 'planned'
    


    for i in range(0,len(index)):
      
        clean_data = {}
        clean_data['careplan_code'] = request.data['careplan_code']
        clean_data['exercise_details'] = request.data['exercise_details']
        clean_data['output_json'] = []
        clean_data['start_date'] = start_date
        clean_data['end_date'] = end_date
        clean_data['output_json'] = output_json
        clean_data['episode_id'] = request.data['pp_ed_id']
        clean_data['time_slot'] = temp
        clean_data["status_flag"] = request.data["status_flag"]
        clean_data['date'] = index[i]
        serilizer = ex_care_planSerializer(data =clean_data)
        if serilizer.is_valid():
            serilizer.save()
        else:
            return Response(serilizer.errors)    
       
    return Response({'message':"care paln added"})





@csrf_exempt
@api_view(['POST'])
def exercise_detail(request):
    
    if 'exercise' in request.data:
        data = ex_exercise_master.objects.filter(title = request.data['exercise'])
        serializer = ex_exercise_master_masterSerializer(data,many = True)
        return Response(serializer.data)
    return Response({"message":"please provise exercise name"})    
    
               



@csrf_exempt
@api_view(['POST','GET'])
def get_care_plan(request):
    if request.method == 'POST':
        try:
            data = ex_care_plan.objects.filter(episode_id = request.data['id'],date=request.data['date'])
            data = ex_care_planSerializer(data,many = True)
          #  data.data[0]['exercise_status'] = data.data[0]['time_slot']
            for i in range(0,len(data.data)):
            
                try:
                    data.data[i]['exercise_status'] = data.data[i]['time_slot']
                    data.data[i]['time_slot'] = list(data.data[i]['time_slot'].keys())
                    for j in data.data[i]['exercise_status'].keys():
                        data.data[i][j] = list(data.data[i]['exercise_status'][j].keys())
                except:
                    pass
            return Response(data.data)
        except:
            return Response(status = status.HTTP_400_BAD_REQUEST)  

    if request.method == "GET":
        try:
            id = request.GET.get("id")
            date = request.GET.get("date")
            data = ex_care_plan.objects.filter(episode_id =id,date=date)
            data = ex_care_planSerializer(data,many = True)
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
@api_view(['POST','GET'])
def get_care_plan_mobile(request):
   # log_info = {}
   # log_info['tran'] = request.COOKIES['tran']
   # log_info['request_body'] = request.data
    if request.method == "POST":
        try:
                
            data = ex_care_plan.objects.filter(episode_id = request.data['id'],date=request.data['date'])
            data = ex_care_planSerializer(data,many = True)
            exercise_data = ex_exercise_master.objects.filter(ex_em_id = data.data[0]['exercise_details'][0]['ex_em_id'])
            exercise_serializer = ex_exercise_master_masterSerializer(exercise_data,many = True)
            data.data[0]['exercises'] = exercise_serializer.data[0]['title']
            response = {}
            time_slot_array = []
            response['time_slot_mobile'] = []
            for i in range(0,len(data.data)):
                data.data[i]['exercise_status'] = data.data[i]['time_slot']
                data.data[i]['time_slot'] = list(data.data[i]['time_slot'].keys())
                data.data[i]['time_slot_mobile'] = {}
                for j in data.data[i]['exercise_status'].keys():
                    data.data[i]['time_slot_mobile'][j] = []
                    if j not in response['time_slot_mobile']:
                        pass
                       # response['time_slot_mobile'][j] = []
                    for k in data.data[i]['exercise_status'][j].keys():
                        temp = {}
                       # temp['exercise_name'] = k
                        temp['time'] = j
                        temp['data'] = []
                     #   print("before")
                        find_or_not = False
                        index = 0
                        for find in range(0,len(response['time_slot_mobile'])):
                           
                            if j in response['time_slot_mobile'][find]['time']:
                                
                                index = find
                                find_or_not = True
                                break
                        if find_or_not:    
                            for l in range(0,len(data.data[i]["exercise_details"])): 
                                    
                                if data.data[i]["exercise_details"][l]['name'] == k:
                                    for m in data.data[i]["exercise_details"][l].keys():
                                        response['time_slot_mobile'][index]['data'].append(data.data[i]["exercise_details"][l])
                                        break
                                # del temp['name']     
                        else:
                            for l in range(0,len(data.data[i]["exercise_details"])):
                            
                                if data.data[i]["exercise_details"][l]['name'] == k:
                                    for m in data.data[i]["exercise_details"][l].keys():
                                        temp['data'].append(data.data[i]["exercise_details"][l])
                                        break        
                            data.data[i]['time_slot_mobile'][j].append(temp)
                            response['time_slot_mobile'].append(temp)
                            response['error'] = False
                            response['message'] = "careplan for selected date is present"
    
            return Response(response)
        except Exception as e:
           
      #      log_info['response_body']  = {"status":400}
       #     logger.info(log_info) 
            return Response({"message":"no care plan for selected date","error":True},status=status.HTTP_200_OK)    
      


    
        


@csrf_exempt
@api_view(['POST'])
def get_all_care_plan(request):
    try:
        data = ex_care_plan.objects.filter(episode_id = request.data['id']).order_by('-date')
        data = ex_care_planSerializer(data,many = True)

        if len(data.data)>0:
            for i in range(0,len(data.data)):
                exercise_data = ex_exercise_master.objects.filter(ex_em_id = data.data[i]['exercise_details'][0]['ex_em_id'])
                exercise_serializer = ex_exercise_master_masterSerializer(exercise_data,many = True)
                data.data[i]['exercises'] = exercise_serializer.data[0]['title']
                time_sl = []
                if type(data.data[i]['time_slot']) == dict:
                    for j in data.data[i]['time_slot'].keys():
                        time_sl.append([j])
                    data.data[i]['time_slot'] = time_sl
       # exercise_data = ex_exercise_master.objects.filter(ex_em_id = data.data[0]['exercise_details'][0]['ex_em_id'])
      #  exercise_serializer = ex_exercise_master_masterSerializer(exercise_data,many = True)
      #  data.data[0]['exercises'] = exercise_serializer.data[0]['title']
        return Response(data.data)
    except :
        
        return Response(status = status.HTTP_400_BAD_REQUEST)    





@csrf_exempt
@api_view(['POST'])
def update_care_plan_status(request):
    try:
        
        data = ex_care_plan.objects.filter(pp_cp_id = request.data['id']).first()
        serializer = ex_care_planSerializer(data)
     #   print(serializer.data['time_slot'])
        request = break_json(request)
        time_keys = request.data['output_json'].keys()
        for i in time_keys:
            ex_keys = request.data['output_json'][i].keys()
       # print("######  ",i,"#########")
            for j in ex_keys:
                serializer.data['time_slot'][i][j] = 'completed'
        for i in time_keys:
            ex_keys = request.data['output_json'][i].keys()
            for j in ex_keys  :
                serializer.data['output_json'][i][j] =request.data['output_json'][i][j]
        # serializer.data['time_slot'][request.data['slot']-1][1] = request.data['status']
        # print(type(serializer.data['output_json']))
        # if "set" in serializer.data['output_json'][0]:
        #     print("insisde")
        #     serializer.data['output_json'].pop(0)
        #     serializer.data['output_json'].append(request.data['output_json'])
        # else:
        #     serializer.data['output_json'].append(request.data['output_json'])    
        # print(serializer.data['time_slot'][request.data['slot']-1][1])

        update = ex_care_planSerializer(data,data=serializer.data,partial=True)
        if update.is_valid():
            update.save()
            return Response({"message":"status updated"})
        else:
            return Response(update.errors)
    except Exception as e:
        #print(e)

        return Response(status = status.HTTP_400_BAD_REQUEST)













def break_json(request):
    output_json = {}
    for i in request.data['output_json'].keys():
        
        output_json[i] = {}

        for j in request.data['output_json'][i].keys():
            
            output_json[i][j] = {}
            output_json[i][j]['rom'] = {}
            output_json[i][j]['set'] = 0
            output_json[i][j]['rep'] = 0


            for k in request.data['output_json'][i][j].keys():
                output_json[i][j]['set']+=1

                
                for l in request.data['output_json'][i][j][k].keys():
                    output_json[i][j]['rep']+=1
                
                    for m in request.data['output_json'][i][j][k][l]['angles'].keys():
                        
                        if m not in output_json[i][j]['rom']:
                            output_json[i][j]['rom'][m] = {}
                            output_json[i][j]['rom'][m]['max'] = request.data['output_json'][i][j][k][l]['angles'][m]['max']
                            output_json[i][j]['rom'][m]['min'] = request.data['output_json'][i][j][k][l]['angles'][m]['min']

                        else:
                            output_json[i][j]['rom'][m]['max'] = max(output_json[i][j]['rom'][m]['max'],request.data['output_json'][i][j][k][l]['angles'][m]['max'])
                            output_json[i][j]['rom'][m]['min'] = max(output_json[i][j]['rom'][m]['min'],request.data['output_json'][i][j][k][l]['angles'][m]['min'])

    request.data['output_json'] = output_json


    return request



