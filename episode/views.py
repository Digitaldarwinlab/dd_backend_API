from django.shortcuts import render
from episode.models import pp_episode_detail,pp_prescription_detail,pp_visit_detail,pp_assessment_detail,pp_notes
from episode.serializer import pp_episode_detailSerializer,pp_prescription_detailSerializer,pp_visit_detailSerializer,pp_assessment_detailSerializer,pp_questionnaire_templateSerializer,pp_notesSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view , schema
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status
import pymongo
import urllib
import datetime
from Physiotherapist.models import pp_physiotherapist_master
from Physiotherapist.serializers import pp_physiotherapist_masterSerializer
from exercise.models import ex_care_plan
from exercise.serializer import ex_care_planSerializer
from patient.models import pp_patient_master
from patient.serializer import pp_patient_master_masterSerializer
import logging
logger = logging.getLogger("info")


myclient = pymongo.MongoClient("mongodb://172.31.0.49:27017")



 

from datetime import date
import json
import random 

@csrf_exempt
@api_view(['POST'])
def add_episode(request):

    db = myclient['Darwin']
    db = db['pp_episode_detail']
    data = request.data
    duplicate = db.find({"pp_pm_id":data["pp_pm_id"]}).sort([("pp_ed_id",-1)])
    if duplicate.count() is not 0:
        duplicate = duplicate[0]
        if duplicate['end_date'] == "":
     
            return Response({"message":"episode for this patient already exist"})
        else:
            sdate = date(int(request.data['start_date'][0:4]), int(request.data['start_date'][-5:-3]), int(request.data['start_date'][-2:]))    
            edate = date(int(duplicate['end_date'][0:4]), int(duplicate['end_date'][-5:-3]), int(duplicate['end_date'][-2:]))    
            if sdate<=edate:
                return Response({"message":"start date should be greater than previous episode"})
            else:
                pass 

            
    maxs = db.find().sort([("pp_ed_id",-1)]).limit(1)[0]["pp_ed_id"]
    serializer = pp_episode_detailSerializer(data = request.data)
    list1 = [1, 2, 3, 4, 5, 6,7,8,9,0]
    if serializer.is_valid():
        #serializer.save()
        data['pp_ed_id'] = maxs+1
        data['episode_number'] = 'e'+ str(random.choice(list1)) + str(maxs+1)
        db.insert_one(data)
        return Response({"message":"episode added"},status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors)


import os        
@csrf_exempt
@api_view(['POST'])
def add_episode_1(request):
    
    #return Response({"message":"ok"})
  #  print(request.FILES)
    log_info = {}
    try:
        log_info['tran'] = request.COOKIES['tran']
    except:
        pass
    log_info['request_body'] = request.data
    db = myclient['Darwin']
    db = db['pp_episode_detail']
    data = {}
    data['pp_pm_id'] = int(request.data['pp_pm_id'])
    
    duplicate = db.find({"pp_pm_id":data["pp_pm_id"]}).sort([("pp_ed_id",-1)])
     
    
    
    if duplicate.count() is not 0:
        duplicate = duplicate[0]
        if duplicate['end_date'] == "": 
            log_info['response_body'] = {"message":"episode for this patient already exist","status":200}
            logger.info(log_info)
            return Response({"message":"episode for this patient already exist"})
        else:
            sdate = date(int(request.data['start_date'][0:4]), int(request.data['start_date'][-5:-3]), int(request.data['start_date'][-2:]))    
            edate = date(int(duplicate['end_date'][0:4]), int(duplicate['end_date'][-5:-3]), int(duplicate['end_date'][-2:]))    
            if sdate<=edate:
                log_info['response_body'] = {"message":"start date should be greater than previous episode","status":200}
                logger.info(log_info)
                return Response({"message":"start date should be greater than previous episode"})
            else:
                pass      
    treating_doctor = pp_patient_master.objects.filter(pk = request.data['pp_pm_id']).first()
    treating_doctor = pp_patient_master_masterSerializer(treating_doctor)
    
    treating_doctor = pp_physiotherapist_master.objects.filter(pp_pm_id = treating_doctor.data['pp_pm']).first()
    treating_doctor = pp_physiotherapist_masterSerializer(treating_doctor)
    
    if len(treating_doctor.data['first_name']) < 1:
        data['treating_doc_details'] = 'admin'
    else:
        data['treating_doc_details'] = treating_doctor.data['first_name']

    maxs = db.find().sort([("pp_ed_id",-1)]).limit(1)[0]["pp_ed_id"]
    if 'PP_Patient_Details' in request.data:
        data['PP_Patient_Details'] = request.data['PP_Patient_Details']
    if 'treating_doc_details' in request.data:    
        data['treating_doc_details'] = request.data['treating_doc_details']
    if 'pp_pm_id' in request.data:    
        data['pp_pm_id'] = int(request.data['pp_pm_id'])
    if 'Operative_Types' in request.data:    
        data['Operative_Types'] = request.data['Operative_Types']
    if 'primary_complaint' in request.data:   
        data['primary_complaint'] = request.data['primary_complaint']
    if 'start_date' in request.data:    
        data['start_date'] = request.data['start_date']
    if 'end_date' in request.data:    
        data['end_date'] = request.data['end_date']
    if 'Patient_History' in request.data:    
        data['Patient_History'] = request.data['Patient_History']
    if 'Closure_Notes' in request.data:    
        data['Closure_Notes'] = request.data['Closure_Notes']
    if 'files' in request.data and request.data['files']!='':
        data['files'] = []

        for i in request.FILES.getlist('files'):
            data['files'].append('https://myphysio.digitaldarwin.in/api/uploadedfiles/'+str(i))   
            path = r"/home/ec2-user/uploadedfiles/" 
            file_name = str(i)
            completeName = os.path.join(path, file_name)
        # file1 = open(request.FILES['files'], "rb")
            files1 = i.read()
        
            file2 = open(completeName,'wb')
        # lines = file1.read()
            
            file2.write(files1)
            file2.close()
    
 
    serializer = pp_episode_detailSerializer(data = request.data)
    list1 = [1, 2, 3, 4, 5, 6,7,8,9,0]
    if serializer.is_valid():
        #serializer.save()
        data['pp_ed_id'] = maxs+1
        data['episode_number'] = 'e'+ str(random.choice(list1)) + str(maxs+1)
        db.insert_one(data)
        log_info['response_body'] = {"message":"episode added","status":201}
        logger.info(log_info)
        return Response({"message":"episode added"},status=status.HTTP_201_CREATED)
    else:
        log_info['response_body'] = serializer.errors
        logger.info(log_info)
        return Response(serializer.errors)    

@csrf_exempt
@api_view(['POST','GET'])
def get_episode(request,id = None):
    log_info = {}
    try:
        log_info['tran'] = request.COOKIES['tran']
    except:
        pass
    log_info['request_body'] = request.data
    db = myclient['Darwin']
    db = db['pp_episode_detail']
    if request.method == "POST":
        result = db.find({"pp_pm_id":request.data['id']}).sort([("pp_ed_id",-1)])
        if result is None:
            log_info['response_body'] = {"message":"data not present","status":200}
            logger.info(log_info)
            return Response({'message':"data not present"})
        data = []    
        for i in result:

            patient = pp_patient_master.objects.filter(pp_patm_id = i['pp_pm_id'])
            patient_serializer = pp_patient_master_masterSerializer(patient,many = True)
        
            physio = pp_physiotherapist_master.objects.filter(pp_pm_id = patient_serializer.data[0]['pp_pm'])
            physio_serializer = pp_physiotherapist_masterSerializer(physio,many = True)
            i['treating_doctor_detail'] = physio_serializer.data
            try:
                i['treating_doc_details_mobile'] = eval(i['treating_doc_details'])
                i['PP_Patient_Details_mobile'] = eval(i['PP_Patient_Details'])
            except:
                pass

            del i['_id']
            data.append(i)

        log_info['response_body'] = data
        logger.info(log_info)
        return Response(data)

    if request.method == 'GET':

        result = db.find({"pp_pm_id":id})
        if result is None:
            return Response({'message':"data not present"})
        data = []
        for i in result:
            patient = pp_patient_master.objects.filter(pp_patm_id = i['pp_pm_id'])
            patient_serializer = pp_patient_master_masterSerializer(patient,many = True)

            physio = pp_physiotherapist_master.objects.filter(pp_pm_id = patient_serializer.data[0]['pp_pm'])
            physio_serializer = pp_physiotherapist_masterSerializer(physio,many = True)
            i['treating_doctor_detail'] = physio_serializer.data

            del i['_id']
            data.append(i)


        return Response(data)

from datetime import date
@csrf_exempt
@api_view(['POST'])
def patient_visit(request):
    db = myclient['Darwin']
    dv = db['pp_visit_detail']
    db = db['pp_episode_detail']
    result = db.find({"pp_pm_id":request.data['id']}).sort([("pp_ed_id",-1)])
    if result.count() == 0:
        return Response(status=status.HTTP_404_NOT_FOUND)

    temp = str(date.today()) 
    to_search = result[0]['pp_ed_id'] 

    result = dv.find({'pp_ed_id':result[0]['pp_ed_id']}).sort([("pp_vd_id",-1)])
    data = []
    for i in result:
        del i['_id']
        data.append(i)

    

    return Response(data)    

    












@csrf_exempt
@api_view(['POST'])
def add_assessment(request):

    db = myclient['Darwin']
    db = db['pp_assessment_detail']
    data = request.data
    maxs = db.find().sort([("pp_ad_id",-1)]).limit(1)[0]["pp_ad_id"]
   # request.data['questionnaires'] = eval(request.data['questionnaires'])
   # request.data['physical_assessement'] = eval(request.data['physical_assessement'])
    serializer = pp_assessment_detailSerializer(data = request.data)
    if serializer.is_valid():
       
        data['pp_ad_id'] = maxs+1
        data['assesmentdate'] = datetime.datetime.utcnow()
        db.insert_one(data)
        return Response({'message':"data added"})
    return Response(serializer.errors)    


    data['pp_ad_id'] = maxs+1
    data['assesmentdate'] = datetime.datetime.utcnow()
    db.insert_one(data)
    
    return Response({'message':"data added"})

    # data = request.data
    # data["physical_assessement"] = json.loads(data["physical_assessement"])
    # serializer = pp_assessment_detailSerializer(data = request.data)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response({'message':"data added"})
    # return Response(serializer.errors)    




@csrf_exempt
@api_view(['POST'])
def add_assessment_1(request):

    db = myclient['Darwin']
    db = db['pp_assessment_detail']
    data = {}
    
    if 'physical_assessement' in request.data:
        data['physical_assessement'] = request.data['physical_assessement']

    if  'questionnaires' in request.data:
        data['questionnaires'] = request.data['questionnaires']  

    if  'pp_ed_id' in request.data:
        
        data['pp_ed_id'] = int(request.data['pp_ed_id'])

    if  'joint1score' in request.data:
        data['joint1score'] = int(request.data['joint1score']) 

    if  'joint2score' in request.data:
        data['joint2score'] = int(request.data['joint2score'])   

    if  'types' in request.data:
        data['types'] = request.data['types']

    if  'AI_data' in request.data:
        data['AI_data'] = request.data['AI_data']    

    if  'Exercise_Name' in request.data:
        data['Exercise_Name'] = request.data['Exercise_Name']

    if  'Numbmess' in request.data:
        data['Numbmess'] = request.data['Numbmess']

    if  "chief_complaint" in request.data:
        data['chief_complaint']  = request.data['chief_complaint']  
    if "complaint_history" in request.data :
        data["complaint_history"] = []
        temp = eval(request.data["complaint_history"])
        for i in temp.keys():
            if temp[i] == 1:
                data["complaint_history"].append([i,1])
            else:
                data["complaint_history"].append([i,0])    
    if "past_medical_history" in request.data:
        data['past_medical_history'] = []
        temp = eval(request.data['past_medical_history'])    
        for i in temp.keys():
            if temp[i] == 1:
                data['past_medical_history'].append([i,1])
            elif i == 'other' and temp[i]!=0:
                data['past_medical_history'].append([i,1,temp[i]])   
            else:
                data['past_medical_history'].append([i,0])     
    if "built_type" in request.data:
        data['built_type'] = []
        temp = request.data['built_type']
        for i in temp.keys():
            if temp[i] == 1:
                data['built_type'].append([i,1])
            else:
                data['built_type'].append([i,0])    

    if "occupation" in request.data:
        data['occupation'] = request.data['occupation']

    if "nature_of_pain" in request.data:
        data['nature_of_pain'] = []
        temp = request.data['nature_of_pain']
        for i in temp.keys():
            if temp[i] == 1:
                data['nature_of_pain'].append([i,1])
            else:
                data['nature_of_pain'].append([i,0])
    if "pain_scale" in request.data:
        data['pain_scale'] = request.data['pain_scale']  

    if "pain_aggravating" in request.data:
        data['pain_aggravating'] = []
        temp = request.data['pain_aggravating']
        for i in temp.keys():
            if temp[i] == 1:
                data['pain_aggravating'].append([i,1])
            else:
                data['pain_aggravating'].append([i,0]) 
    if "pain_relieving" in request.data:
        data['pain_relieving'] = []
        temp = request.data['pain_relieving']
        for i in temp.keys():
            if temp[i] == 1:
                data['pain_relieving'].append([i,1])
            else:
                data['pain_relieving'].append([i,0]) 
    if "shoulder" in request.data:
        data['shoulder'] = []
        temp = eval(request.data['shoulder'])
        for i in temp.keys():
            
            data['shoulder'].append([i,request.data[i]])
    if "Elbow" in request.data:
        data["Elbow"] = []
        temp = eval(request.data["Elbow"])
        for i in temp.keys():
            
            data["Elbow"].append([i,request.data[i]])
    if "Forearm, wrist & Hand" in request.data:
        data['shoulder'] = []
        temp = eval(request.data['Forearm, wrist & Hand'])
        for i in temp.keys():
            
            data['Forearm, wrist & Hand'].append([i,request.data[i]])
                     
    if "Hip" in request.data:
        data["Hip"] = []
        temp = eval(request.data["Hip"])
        for i in temp.keys():
            
            data["Hip"].append([i,request.data[i]])
                     
    if "Knee" in request.data:
        data["Knee"] = []
        temp = eval(request.data["Knee"])
        for i in temp.keys():
            
            data["Knee"].append([i,request.data[i]])
                     
    if "Ankle" in request.data:
        data["Knee"] = []
        temp = eval(request.data["Ankle"])
        for i in temp.keys():
            
            data["Ankle"].append([i,request.data[i]])
                     
    if "Cervical Spine" in request.data:
        data["Cervical Spine"] = []
        temp = eval(request.data["Cervical Spine"])
        for i in temp.keys():
            
            data["Cervical Spine"].append([i,request.data[i]])
                     
    if "Thoracic Spine" in request.data:
        data["Thoracic Spine"] = []
        temp = eval(request.data["Thoracic Spine"])
        for i in temp.keys():
            
            data["Thoracic Spine"].append([i,request.data[i]])
                     
    if "Lumbar Spine" in request.data:
        data["Lumbar Spine"] = []
        temp = eval(request.data["Lumbar Spine"])
        for i in temp.keys():
            
            data["Lumbar Spine"].append([i,request.data[i]])
                     




    if 'ScareFile' in request.data and request.data['ScareFile']!='':
        data['ScareFile'] = []
        for i in request.FILES.getlist('ScareFile'):
            data['ScareFile'].append(r'C:\Users\sc\Desktop\Darwin_backend\backend\clinic/'+str(i))
            path = r"C:\Users\sc\Desktop\Darwin_backend\backend\clinic"
            file_name = str(i)
            completename = os.path.join(path,file_name)
            file1 = i.read()
            file2 = open(completename,'wb') 
            file2.write(file1)
            file2.close()
    if 'TraumaFile' in request.data and request.data['TraumaFile']!='':
        data['TraumaFile'] = []
        for i in request.FILES.getlist('TraumaFile'):
            data['TraumaFile'].append(r'C:\Users\sc\Desktop\Darwin_backend\backend\clinic/'+str(i))
            path = r"C:\Users\sc\Desktop\Darwin_backend\backend\clinic"
            file_name = str(i)
            completename = os.path.join(path,file_name)
            file1 = i.read()
            file2 = open(completename,'wb')
            file2.write(file1)
            file2.close()



       

           



    maxs = db.find().sort([("pp_ad_id",-1)]).limit(1)[0]["pp_ad_id"]
   # request.data['questionnaires'] = eval(request.data['questionnaires'])
   # request.data['physical_assessement'] = eval(request.data['physical_assessement'])
    serializer = pp_assessment_detailSerializer(data = request.data)
    if serializer.is_valid():
       
        data['pp_ad_id'] = maxs+1
        data['assesmentdate'] = datetime.datetime.utcnow()
        db.insert_one(data)
        return Response({'message':"data added"})
    return Response(serializer.errors)    


    data['pp_ad_id'] = maxs+1
    data['assesmentdate'] = datetime.datetime.utcnow()
    db.insert_one(data)
    
    return Response({'message':"data added"})    






@csrf_exempt
@api_view(['POST'])
def questions(request):
    db = myclient['Darwin']
    db = db['pp_questionnaire_template']
    data = request.data
    maxs = db.find().sort([("pp_qt_id",-1)]).limit(1)[0]["pp_qt_id"]

    serializer = pp_questionnaire_templateSerializer(data = request.data)
    if serializer.is_valid():
        data['pp_qt_id'] = maxs+1
        db.insert_one(data)
        return Response({'message':"data added"})

    return Response(serializer.errors)    

    data['pp_qt_id'] = maxs+1
    db.insert_one(data)
    return Response({'message':"data added"})



@csrf_exempt
@api_view(['POST'])
def get_assessment(request):
    db = myclient['Darwin']
    db = db['pp_assessment_detail']
    result = db.find_one({"pp_ed_id":request.data['id']})
    data = []
    if result is None:
        return Response({'message':"data not present"})
   # for  i in result:
     #   del i['_id']   
    #    data.append(i)
    del result['_id']
   # result = data

    return Response(result)






@csrf_exempt
@api_view(['POST'])
def add_visit(request):
    db = myclient['Darwin']
    db = db['pp_visit_detail']
    data = request.data
   # print(data)
    maxs = db.find().sort([("pp_vd_id",-1)]).limit(1)[0]["pp_vd_id"]
   
        


    for i in range(0,len(data)):
        serializer = pp_visit_detailSerializer(data = data[i])
        if serializer.is_valid():
            pass
        else:
            return Response(serializer.errors)
    
    
    for i in range(0,len(data)):
        data[i]["pp_vd_id"] = maxs+1
      #  data[i]['appointment_detail']['startDate'] = data[i]['appointment_detail']['startDate'][:10]
        maxs+=1
 
    try:   
        db.insert_many(data)
        return Response({'message':"data added"})
    except exceptions as e:
        return Response(e)
    
 

@csrf_exempt
@api_view(['POST','GET'])
def get_visit(request,id = None):
    db = myclient['Darwin']
    de = db['pp_episode_detail']
    db = db['pp_visit_detail']
    if request.method == 'POST':
        result = db.find({"pp_ed_id":request.data['id']})
        if result is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data =[]
        for i in result:
            del i['_id']   
            data.append(i) 

        for i in range(0,len(data)):
            e = de.find_one({"pp_ed_id":data[i]['pp_ed_id']})
            serializer = pp_patient_master.objects.filter(pp_patm_id = e['pp_pm_id'])
            serializer = pp_patient_master_masterSerializer(serializer,many = True)
            data[i]['patient_datail'] = serializer.data
   
    
    
        return Response(data)
    if request.method == 'GET':
        result = db.find({"pp_ed_id":id})
        if result is None:
            return Response({'message':"data not present"})
        data =[]
        for i in result:
            del i['_id']
            data.append(i)

        for i in range(0,len(data)):
            e = de.find_one({"pp_ed_id":data[i]['pp_ed_id']})
            serializer = pp_patient_master.objects.filter(pp_patm_id = e['pp_pm_id'])
            serializer = pp_patient_master_masterSerializer(serializer,many = True)
            data[i]['patient_datail'] = serializer.data
        return Response(data)





@csrf_exempt
@api_view(['POST'])
def get_visit_by_physio(request):
    db = myclient['Darwin']
    de = db['pp_episode_detail']
    db = db['pp_visit_detail']
    result = db.find({"created_by":request.data['id']})
   
    if result is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data =[]
    for i in result:
        
        del i['_id']   
        data.append(i) 
    for i in range(0,len(data)):
        try:
            e = de.find_one({"pp_ed_id":data[i]['pp_ed_id']})
            serializer = pp_patient_master.objects.filter(pp_patm_id = e['pp_pm_id'])
            serializer = pp_patient_master_masterSerializer(serializer,many = True)
            data[i]['patient_datail'] = serializer.data
        except:
            pass
   
   
    return Response(data)




@csrf_exempt
@api_view(['POST'])
def update_episode(request):
    db = myclient['Darwin']
    db = db['pp_episode_detail']
    
    serializer = pp_episode_detailSerializer(data = request.data)
    if serializer.is_valid():
        code = db.find_one({"pp_ed_id":request.data['pp_ed_id']})
        request.data['episode_number'] = code['episode_number']
        if 'files' in code:
            request.data['files'] = code['files']
        db.update(
            {"pp_ed_id":request.data['pp_ed_id']},
            request.data
        )
        return Response({"message":"episode updated"})
    return Response(serializer.errors)    


@csrf_exempt
@api_view(['POST'])
def update_visit(request):
    db = myclient['Darwin']
    db = db['pp_visit_detail']
    serializer = pp_visit_detailSerializer(data = request.data)
    if serializer.is_valid():
        db.update(
            {"pp_vd_id":request.data['pp_vd_id']},
            request.data
        )
        return Response({"message":"episode updated"})
    return Response(serializer.errors)    



@csrf_exempt
@api_view(['POST'])
def add_pres(request):
    db = myclient['Darwin']
    db = db['pp_prescription_detail']
    data = request.data
    maxs = db.find().sort([("pp_pres_id",-1)]).limit(1)[0]["pp_pres_id"]
    serializer = pp_prescription_detailSerializer(data = data)
    if serializer.is_valid():
        data['pp_pres_id'] = maxs + 1
        db.insert_one(data)
        return Response({"message":"prescription added"},status=status.HTTP_201_CREATED)
    return Response(serializer.errors)    





@csrf_exempt
@api_view(['POST'])
def dashboard(request):
    db = myclient['Darwin']
    da = db['pp_assessment_detail']
    dp = db['pp_prescription_detail']
    db = db['pp_episode_detail']
  
    physio = pp_physiotherapist_master.objects.all()
    data = pp_physiotherapist_masterSerializer(physio,many = True)
           
    response = {}
    for i in data.data:
          
        
        try:    
            patient  = pp_patient_master.objects.filter(pp_pm = i['pp_pm_id'])
            
            serilizer = pp_patient_master_masterSerializer(patient, many = True)
            if patient.count()>0:
                for z in range(0,patient.count()):
                    
                    epi = db.find({'pp_pm_id':serilizer.data[z]['pp_patm_id']})
                    if epi.count()>0:
                        ep = []
                        for j in epi:
                            
                            del j['_id']
                            asse = da.find({'pp_ed_id':j['pp_ed_id']})
                            if asse.count()>0:
                                for q in asse:
                                    del q['_id']
                                    j['assessment'] = q

                            pres =  dp.find({"pp_ed_id":j['pp_ed_id']})
                            if pres.count()>0:
                                for p in pres:
                                    del p['_id']
                                    j['prescription'] = p        
                            ep.append(j)

                            care = ex_care_plan.objects.filter(episode_id = j['pp_ed_id'])
                            print(care.count())
                            if care.count()>0:
                                print(care)
                                care = ex_care_planSerializer(care,many = True)
                                print(care.data)
                                j['care_plan'] = care.data



                    serilizer.data[z]['episode'] = ep        
            
            response[i['pp_pm_id']] = serilizer.data
           
        except:
            pass    
            
        

    #print(response)   
    
    return Response(response) 
    
    
    
@csrf_exempt
@api_view(['POST'])
def add_notes(request):
    db = myclient['Darwin']
    db = db['pp_notes']
    data = request.data
    maxs = db.find().sort([("no_id",-1)]).limit(1)[0]["no_id"]
    serializer = pp_notesSerializer(data = request.data)
    if serializer.is_valid():
        data["no_id"] = maxs + 1
        db.insert_one(data)
        return Response({"message":"episode added"},status=status.HTTP_201_CREATED)
    return Response(serializer.errors)    



@csrf_exempt
@api_view(['POST'])
def get_notes(request):
    db = myclient['Darwin']
    db = db['pp_notes']

    result = db.find({"eid":request.data['id']})
    if result is None:
        return Response({'message':"data not present"})
    data = []    
    for i in result:
        del i['_id']
        data.append(i)

   
    return Response(data)



@csrf_exempt
@api_view(['POST'])
def get_question(request):
    db = myclient['Darwin']
    db = db['pp_questionnaire_template']
    try:
        data  =   db.find_one({'template_name':request.data['query']})
        del data['_id']
       
        return Response(data)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)    





@csrf_exempt
@api_view(['POST'])
def get_active_episode(request):
    db = myclient['Darwin']
    db = db['pp_episode_detail']
    result = db.find({"pp_pm_id":request.data['id'],"status_flag":"1"})
    if result is None:
        return Response({'message':"data not present"})
    data = []    
    for i in result:
        del i['_id']
        data.append(i)

   
    return Response(data)








@csrf_exempt
@api_view(['POST'])
def patient_assessment(request):
    db = myclient['Darwin']
    da = db['pp_assessment_detail']
    db = db['pp_episode_detail']
    try:
        patient_id = db.find({"pp_pm_id":request.data['id']}).sort([("pp_ed_id",-1)])
        patient_id = patient_id[0]
    
        assessment_data = da.find({"pp_ed_id":patient_id['pp_ed_id']})
        data = []
        for i in assessment_data:
            del i['_id']
            data.append(i)
       # del assessment_data['_id']
        return Response(data)
    except:
        return Response(status = status.HTTP_400_BAD_REQUEST)













@csrf_exempt
@api_view(['POST'])
def get_pres(request):

    db = myclient['Darwin']
    db = db['pp_prescription_detail']
    try:
        response = []
        data = db.find({'pp_ed_id':request.data['id']}).sort([("pp_ed_id",-1)])
        if data is None:
            return Response({'message':"data not present"})
        for i in data:    
            del i['_id'] 
            response.append(i)
        return Response(response)   

    except Exception as e:
        return Response(status=status.HTTP_404_NOT_FOUND)




   






@csrf_exempt
@api_view(['POST'])
def patient_dashboard(request):
    db = myclient['Darwin']
    da = db['pp_assessment_detail']
    dp = db['pp_prescription_detail']
    db = db['pp_episode_detail']

    response = {}

    try:
        patient = pp_patient_master.objects.filter(
            pp_patm_id=request.data['id'])

        serilizer = pp_patient_master_masterSerializer(patient, many=True)
        response['first_name'] = serilizer.data[0]['first_name']
        response['last_name'] = serilizer.data[0]['last_name']
        response['blood_group'] = serilizer.data[0]['blood_group']
        response['dob'] = serilizer.data[0]['dob']
        response['mobile_no'] = serilizer.data[0]['mobile_no']
        response['whatsapp_no'] = serilizer.data[0]['whatsapp_no']
        response['allergy_detail'] = serilizer.data[0]['allergy_detail']
        response['gender'] = serilizer.data[0]['gender']
        response['patient_id'] = serilizer.data[0]['pp_patm_id']
        response['treating_doc_id'] = serilizer.data[0]['pp_pm']
        response['patient_code'] = serilizer.data[0]['patient_code']
        response['email'] = serilizer.data[0]['email']
        response['episode'] = {}
        response['assessment'] = {}
        response['care_plan'] = {}
        response['KPIs'] = {}
        response['KPIs']['patient ROM analysis with min and max score'] = {}
        response['KPIs']['care plan exercise analysis'] = {}

     #  print(patient.count())
        if patient.count() > 0:
            for z in range(0, patient.count()):
               # print(serilizer.data[z])

                epi = db.find({'pp_pm_id': serilizer.data[z]['pp_patm_id']})
               # print(epi.count())
                if epi.count() > 0:
                    ep = []
                    for j in epi:

                        del j['_id']
                        response['episode']['episode_id'] = j['pp_ed_id']
                        response['episode']['primary_complaint'] = j['primary_complaint']
                        response['episode']['episode_number'] = j['episode_number']
                        response['episode']['start_date'] = j['start_date']
                        response['episode']['Closure_Notes'] = j['Closure_Notes']
                        response['episode']['patient_code'] = serilizer.data[0]['patient_code']
                        response['episode']['patient_id'] = serilizer.data[0]['pp_patm_id']
                        asse = da.find({'pp_ed_id': j['pp_ed_id']})
                        if asse.count() > 0:
                            for q in asse:
                                del q['_id']
                                j['assessment'] = q
                           #     print(q)
                            #    print(type(q["physical_assessement"]))
                                if type(q["physical_assessement"]) == str:
                                    response['assessment']['scars'] = eval(
                                        q["physical_assessement"])['Scars']
                                    response['assessment']['pain_meter'] = eval(
                                        q["physical_assessement"])['PainMeter']
                                    response['assessment']['RecentHistory'] = eval(
                                        q["physical_assessement"])['RecentHistory']

                                else:
                                 #   print(q["physical_assessement"]['Scars'])
                                    response['assessment']['scars'] = q["physical_assessement"]['Scars']
                                    response['assessment']['pain_meter'] = q["physical_assessement"]['PainMeter']
                                    response['assessment']['RecentHistory'] = q["physical_assessement"]['RecentHistory']

                                response['assessment']['Symptoms_koos_score'] = q["questionnaires"]['Symptoms'][3]
                                response['assessment']['Stiffness_koos_score'] = q["questionnaires"]['Stiffness'][3]
                                response['assessment']['pain_koos_score'] = q["questionnaires"]['pain'][3]
                                response['assessment']['DailyLiving_koos_score'] = q["questionnaires"]['DailyLiving'][3]
                                response['assessment']['Sports_koos_score'] = q["questionnaires"]['Sports'][3]
                                response['assessment']['Life_koos_score'] = q["questionnaires"]['Life'][3]
                                response['assessment']['patient_code'] = serilizer.data[0]['patient_code']
                                response['assessment']['patient_id'] = serilizer.data[0]['pp_patm_id']
                                response['assessment']['types'] = q['types']
                                response['assessment']['ROM'] = q['AI_data']

                        pres = dp.find({"pp_ed_id": j['pp_ed_id']})
                        if pres.count() > 0:
                            for p in pres:
                                del p['_id']
                                j['prescription'] = p
                        ep.append(j)

                        care = ex_care_plan.objects.filter(
                            episode_id=j['pp_ed_id']).order_by('date')
                        care_serializer = ex_care_planSerializer(
                            care, many=True)
                     #   print(care.count())
                        total_exercise = 0
                        pending_exercise = 0
                        completed_exercise = 0
                        if care.count() > 0:
                           # print(care)
                            for plan in range(0, care.count()):
                                total_exercise += len(
                                    care_serializer.data[plan]['time_slot'])
                               # print(care_serializer.data[plan]['time_slot'])
                                #keys = care_serializer.data[0]['output_json'].keys()
                                response['KPIs']['patient ROM analysis with min and max score'][care_serializer.data[plan]['date']] = {
                                }
                                response['KPIs']['care plan exercise analysis'][care_serializer.data[plan]['date']] = {
                                }
                                for detail in range(0, len(care_serializer.data[plan]['exercise_details'])):
                                    response['KPIs']['patient ROM analysis with min and max score'][care_serializer.data[plan]
                                                                                                    ['date']]['joint'] = care_serializer.data[plan]['exercise_details'][detail]['Rom']['joint']
                                    response['KPIs']['patient ROM analysis with min and max score'][care_serializer.data[plan]
                                                                                                    ['date']]['max_angle'] = care_serializer.data[plan]['exercise_details'][detail]['Rom']['max']
                                    response['KPIs']['patient ROM analysis with min and max score'][care_serializer.data[plan]
                                                                                                    ['date']]['min_angle'] = care_serializer.data[plan]['exercise_details'][detail]['Rom']['min']
                                    exercise_data = ex_exercise_master.objects.filter(
                                        ex_em_id=care_serializer.data[plan]['exercise_details'][detail]["ex_em_id"])

                                    for output in range(0, len(care_serializer.data[plan]["output_json"])):
        #                                print("before")

                                        if "set" not in care_serializer.data[plan]['output_json'][0]:

                                            response['KPIs']['patient ROM analysis with min and max score'][care_serializer.data[plan]
                                                                                                            ['date']]['slot'+str(output+1)] = care_serializer.data[plan]['output_json'][output]

                                #    perform_by_patient_keys = care_serializer.data[plan]['output_json'].keys()
                                #    for perform in perform_by_patient_keys:
                                #        perform_angle = care_serializer.data[plan]['output_json'][perform]['angles'].keys()
                                #        response['KPIs']['patient ROM analysis with min and max score'][care_serializer.data[plan]['date']]['Rep'] = care_serializer.data[plan]['output_json'][perform]['Rep']
                                #        for perform_angle_ in perform_angle:
                                #            response['KPIs']['patient ROM analysis with min and max score'][care_serializer.data[plan]['date']][perform_angle_] = {}

                                #            response['KPIs']['patient ROM analysis with min and max score'][care_serializer.data[plan]['date']][perform_angle_]['max_angle_perform'] = care_serializer.data[plan]['output_json'][perform]['angles'][perform_angle_]['max']
                                #            response['KPIs']['patient ROM analysis with min and max score'][care_serializer.data[plan]['date']][perform_angle_]['min_angle_perform'] = care_serializer.data[plan]['output_json'][perform]['angles'][perform_angle_]['min']

                                    exercise_data = ex_exercise_master_masterSerializer(
                                        exercise_data, many=True)
                                #   print(care_serializer.data[plan]['date'] )
                                    response['KPIs']['patient ROM analysis with min and max score'][care_serializer.data[plan]
                                                                                                    ['date']]['exercise_name'] = exercise_data.data[0]['title']
                                #   response['KPIs']['patient ROM analysis with min and max score'][care_serializer.data[plan]['date']]['sets'] = care_serializer.data[plan]['exercise_details'][detail]['Rep']

                                for pen in range(0, len(care_serializer.data[plan]['time_slot'])):
                                    if care_serializer.data[plan]['time_slot'][pen][1] == 'pending' or care_serializer.data[plan]['time_slot'][pen][1] == 'planned':
                                        pending_exercise += 1
                                    if care_serializer.data[plan]['time_slot'][pen][1] == 'completed':
                                        completed_exercise += 1

                        response['KPIs']['care plan exercise analysis']['start_date'] = care_serializer.data[0]['date']
                        response['KPIs']['care plan exercise analysis']['end_date'] = care_serializer.data[care.count(
                        )-1]['date']
                        response['care_plan']['total_exercise'] = total_exercise
                        response['care_plan']['pending_exercise'] = pending_exercise
                        response['care_plan']['completed_exercise'] = completed_exercise
                        response['care_plan']['care_plan_code'] = care_serializer.data[0]['careplan_code']
                        response['care_plan']['episode_id'] = care_serializer.data[0]['episode_id']
                        response['care_plan']['start_date'] = care_serializer.data[0]['date']
                        response['care_plan']['end_date'] = care_serializer.data[care.count(
                        )-1]['date']
                        response['care_plan']['patient_id'] = serilizer.data[0]['pp_patm_id']
                        response['care_plan']['slot_per_day'] = len(
                            care_serializer.data[0]['time_slot'])
                        response['care plan completion %'] = float(
                            (completed_exercise/total_exercise))*100

                serilizer.data[z]['episode'] = ep

       # response = serilizer.data

    except Exception as e:
        
        pass

    # print(response)

    return Response(response) 













@csrf_exempt
@api_view(['POST'])
def progress(request):
 #   print(datetime.date.today()-datetime.timedelta(days=3))
    db = myclient['Darwin']
    da = db['pp_assessment_detail']
    db = db['pp_episode_detail']
    response = {}
    try:
        patient = pp_patient_master.objects.filter(
            pp_patm_id=request.data['id'])
        patient_serializer = pp_patient_master_masterSerializer(
            patient, many=True)
        episode = db.find_one(
            {'pp_pm_id': patient_serializer.data[0]['pp_patm_id']})
    
        care_plan = ex_care_plan.objects.filter(
            episode_id=episode['pp_ed_id']).order_by('date')
        care_plan_serializer = ex_care_planSerializer(care_plan, many=True)
        try:
            episode = db.find_one(
                {'pp_pm_id': patient_serializer.data[0]['pp_patm_id']})
            assessment = da.find_one({'pp_ed_id': episode['pp_ed_id']})
          #  print(assessment)
            if type(assessment["physical_assessement"]) == str:
                response['scars'] = eval(
                    assessment["physical_assessement"])['Scars']
                response['pain_meter'] = eval(
                    assessment["physical_assessement"])['PainMeter']
                response['RecentHistory'] = eval(assessment["physical_assessement"])[
                    'RecentHistory']

            else:
                #   print(q["physical_assessement"]['Scars'])
                response['scars'] = assessment["physical_assessement"]['Scars']
                response['pain_meter'] = assessment["physical_assessement"]['PainMeter']
                response['RecentHistory'] = assessment["physical_assessement"]['RecentHistory']

            response['Symptoms_koos_score'] = assessment["questionnaires"]['Symptoms'][3]
            response['Stiffness_koos_score'] = assessment["questionnaires"]['Stiffness'][3]
            response['pain_koos_score'] = assessment["questionnaires"]['pain'][3]
            response['DailyLiving_koos_score'] = assessment["questionnaires"]['DailyLiving'][3]
            response['Sports_koos_score'] = assessment["questionnaires"]['Sports'][3]
            response['Life_koos_score'] = assessment["questionnaires"]['Life'][3]
        except Exception as e:
            pass
 #           print(e)

        for index in range(0, care_plan.count()):
           # print(datetime.datetime.strptime(care_plan_serializer.data[index]['date'],'%Y-%m-%d') -datetime.timedelta(days=3))
            response[care_plan_serializer.data[index]['date']] = {}
            for exer in care_plan_serializer.data[index]['exercise_details']:

                response[care_plan_serializer.data[index]
                         ['date']][exer['name']] = {}
                response[care_plan_serializer.data[index]['date']][exer['name']]['allocated_rep'] = int(
                    exer['Rep']['rep_count'])*len(care_plan_serializer.data[index]['time_slot'])
                response[care_plan_serializer.data[index]['date']][exer['name']]['allocated_set'] = int(
                    exer['Rep']['set'])*len(care_plan_serializer.data[index]['time_slot'])
                response[care_plan_serializer.data[index]['date']
                         ][exer['name']]['targetted_max'] = exer['Rom']['max']
                target_max = response[care_plan_serializer.data[index]
                                      ['date']][exer['name']]['targetted_max']
                response[care_plan_serializer.data[index]['date']
                         ][exer['name']]['targetted_min'] = exer['Rom']['min']
                target_min = response[care_plan_serializer.data[index]
                                      ['date']][exer['name']]['targetted_min']
                response[care_plan_serializer.data[index]['date']
                         ][exer['name']]['primary joint'] = exer['Rom']['joint']
                #response[care_plan_serializer.data[index]['date']][exer['name']]['achieve_set'] = 0
                response[care_plan_serializer.data[index]
                         ['date']][exer['name']]['achieve_rep'] = 0
                response[care_plan_serializer.data[index]['date']][exer['name']]['achieve_set'] = 0
             #   response[care_plan_serializer.data[index]['date']][exer['name']]['ROM'] = {}
                s = response[care_plan_serializer.data[index]
                             ['date']][exer['name']]['primary joint']
                slot = 1
                min_accu = 0
                max_accu = 0
                if "set" not in care_plan_serializer.data[index]['output_json']:
                    for execut in care_plan_serializer.data[index]['output_json'].keys():
#                        print("before")
                       # if execut['squat']:
                        #  print(1)
                     #   response[care_plan_serializer.data[index]['date']][exer['name']]['achieve_set']+= execut[exer['name']]['Rep']['set']
                        response[care_plan_serializer.data[index]['date']][exer['name']
                                                                           ]['achieve_rep'] += care_plan_serializer.data[index]['output_json'][execut][exer['name']]['rep']
                        response[care_plan_serializer.data[index]['date']][exer['name']]['achieve_set']+= care_plan_serializer.data[index]['output_json'][execut][exer['name']]['set']
                        response[care_plan_serializer.data[index]['date']][exer['name']
                                                                           ][execut] = care_plan_serializer.data[index]['output_json'][execut][exer['name']]
                      #  del response[care_plan_serializer.data[index]['date']][exer['name']]['ROM']['slot '+str(slot)]['Rep']
                        max_accu += response[care_plan_serializer.data[index]
                                             ['date']][exer['name']][execut]['rom'][s]['max']
                        min_accu += response[care_plan_serializer.data[index]
                                             ['date']][exer['name']][execut]['rom'][s]['min']
                    #    slot+=1
                    max_accu = (abs(target_max - max_accu)/target_max)*100
                    min_accu = (abs(target_min - min_accu)/target_min)*100
                    response[care_plan_serializer.data[index]['date']
                             ][exer['name']]['max_accuracy'] = max_accu
                    response[care_plan_serializer.data[index]['date']
                             ][exer['name']]['min_accuracy'] = min_accu
                response[care_plan_serializer.data[index]['date']][exer['name']]['rep_completion %'] = (
                    response[care_plan_serializer.data[index]['date']][exer['name']]['achieve_rep']/response[care_plan_serializer.data[index]['date']][exer['name']]['allocated_rep'])*100
                response[care_plan_serializer.data[index]['date']][exer['name']]['set_completion %'] = (
                    response[care_plan_serializer.data[index]['date']][exer['name']]['achieve_set']/response[care_plan_serializer.data[index]['date']][exer['name']]['allocated_set'])*100
             #   response[care_plan_serializer.data[index]['date']][exer['name']]['set_completion %'] = (response[care_plan_serializer.data[index]['date']][exer['name']]['achieve_set']/response[care_plan_serializer.data[index]['date']][exer['name']]['allocated_set'])*100

    except Exception as e:
      #  print(e)
        pass

    return Response(response)













@csrf_exempt
@api_view(['GET'])
def test_get_visit(request,pk = None):
    db = myclient['Darwin']
    de = db['pp_episode_detail']
    db = db['pp_visit_detail']
    result = db.find({"pp_ed_id":pk})
    if result is None:
        return Response({'message':"data not present"})
    data =[]
    for i in result:
        del i['_id']   
        data.append(i) 

    for i in range(0,len(data)):
        e = de.find_one({"pp_ed_id":data[i]['pp_ed_id']})
        serializer = pp_patient_master.objects.filter(pp_patm_id = e['pp_pm_id'])
        serializer = pp_patient_master_masterSerializer(serializer,many = True)
        data[i]['patient_datail'] = serializer.data
   
    
    #print(data[0]['pp_ed_id'])
    return Response(data)

from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

@csrf_exempt
@api_view(['POST'])
def insert_asse_test(request):
    db = myclient['Darwin']
    
    db = db['assessment_test']
    maxs = db.find().sort([("as_te_id",-1)]).limit(1)[0]["as_te_id"]
    data = request.data
    data['result'] =eval(urlsafe_base64_decode(data['result']))
    data['as_te_id'] = maxs+1
    db.insert_one(data)
    return Response({"data addedd"})






@csrf_exempt
@api_view(['POST'])
def get_asse_test(request):
    db = myclient['Darwin']
    
    db = db['assessment_test']
    
    data = db.find_one({"as_te_id" : request.data['id']})
    del data['_id']
    
    
    
    
    return Response(data)







@csrf_exempt
@api_view(['POST'])
def delete_visit(request):
    db = myclient['Darwin']
    dv = db['pp_visit_detail']
    try:
        dv.delete_one({"pp_vd_id":request.data['id']})
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
#        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)






@csrf_exempt
@api_view(['POST'])
def progress_1(request):
 #   print(datetime.date.today()-datetime.timedelta(days=3))
    db = myclient['Darwin']
    da = db['pp_assessment_detail']
    db = db['pp_episode_detail']
    response = {}
    try:
        patient                   = pp_patient_master.objects.filter(pp_patm_id = request.data['id'])
        patient_serializer        = pp_patient_master_masterSerializer(patient, many = True)
        episode                   = db.find_one({'pp_pm_id':patient_serializer.data[0]['pp_patm_id']})
    #    episode                   = episode[0]
     #   print(episode['pp_ed_id'])
        care_plan                 = ex_care_plan.objects.filter(episode_id = episode['pp_ed_id']).order_by('date')
        care_plan_serializer      = ex_care_planSerializer(care_plan,many = True)
      #  print(care_plan.count())
        try:
       #     print("########### before assessment #################")
         #   episode = db.find_one({'pp_pm_id':patient_serializer.data[0]['pp_patm_id']})
            assessment = da.find_one({'pp_ed_id':episode['pp_ed_id']})
          #  print(assessment)
            if type(assessment["physical_assessement"]) == str:
              #  print("########### after assessment #################")
                response['scars'] = eval(assessment["physical_assessement"])['Scars']
                response['pain_meter'] = eval(assessment["physical_assessement"])['PainMeter']
                response['RecentHistory'] = eval(assessment["physical_assessement"])['RecentHistory']

            else:
                                 #   print(q["physical_assessement"]['Scars'])
                response['scars'] = assessment["physical_assessement"]['Scars']
                response['pain_meter'] = assessment["physical_assessement"]['PainMeter']
                response['RecentHistory'] = assessment["physical_assessement"]['RecentHistory']

            response['Symptoms_koos_score'] = assessment["questionnaires"]['Symptoms'][3]
            response['Stiffness_koos_score'] = assessment["questionnaires"]['Stiffness'][3]
            response['pain_koos_score'] = assessment["questionnaires"]['pain'][3]
            response['DailyLiving_koos_score'] = assessment["questionnaires"]['DailyLiving'][3]
            response['Sports_koos_score'] = assessment["questionnaires"]['Sports'][3]
            response['Life_koos_score'] = assessment["questionnaires"]['Life'][3]
        except Exception as e:
        #    print(e)
            pass
                
        response['data_vertical_bar'] = []
        response['data_vertical_bar2'] = []
        response['data_line'] = []
        target_min = {}
        target_max = {}
        current_min = {}
        current_max = {}

        target_min['id'] = 'Target_Min'
        target_max['id'] = 'Target_Max'
        current_min['id'] = 'current_Min'
        current_max['id'] = 'current_Max'


        target_min['color'] = 'hsl(19, 70%, 50%)'
        target_max['color'] = 'hsl(19, 70%, 50%)'
        current_min['color'] = 'hsl(5, 70%, 50%)'
        current_max['color'] = 'hsl(5, 70%, 50%)'

        target_min['data'] =  []
        target_max['data'] =  []
        current_min['data'] = []
        current_max['data'] = []
        total_exercise = 0
        exercise_done = 0
        new_data = {}
        for index in range(0,care_plan.count()):
            today_total = 0
            today_done = 0
            today_total+= len(care_plan_serializer.data[index]['exercise_details']) * len(care_plan_serializer.data[index]['time_slot'].keys())
            total_exercise+= len(care_plan_serializer.data[index]['exercise_details']) * len(care_plan_serializer.data[index]['time_slot'].keys())
            temp_2 = {}
            new_data[care_plan_serializer.data[index]['date']] = {}
            temp_2['Date'] = care_plan_serializer.data[index]['date']
            temp_2['SetCompletionRate'] = 0
            temp_2['SetCompletionRateColor'] = 'hsl(18, 70%, 50%)'
           # print(ex_care_planSerializer.data[index])
            for time in care_plan_serializer.data[index]['output_json'].keys():
         #       print("######## satwik")
          #      print(time)
                for exercise in care_plan_serializer.data[index]['output_json'][time].keys():
                    exercise_done+=1
                    today_done+=1
                    temp_2['SetCompletionRate']+= (care_plan_serializer.data[index]['output_json'][time][exercise]['set'] * care_plan_serializer.data[index]['output_json'][time][exercise]['rep'])
                    for joint in care_plan_serializer.data[index]['output_json'][time][exercise]['rom'].keys():
                        if joint not in new_data[care_plan_serializer.data[index]['date']]:
                            new_data[care_plan_serializer.data[index]
                                     ['date']][joint] = {}
                            new_data[care_plan_serializer.data[index]
                                     ['date']][joint]['min'] = 1000
                            new_data[care_plan_serializer.data[index]
                                     ['date']][joint]['max'] = -1
                        new_data[care_plan_serializer.data[index]['date']][joint]['min'] = min(
                            new_data[care_plan_serializer.data[index]['date']][joint]['min'], care_plan_serializer.data[index]['output_json'][time][exercise]['rom'][joint]['min'])
                        new_data[care_plan_serializer.data[index]['date']][joint]['max'] = max(
                            new_data[care_plan_serializer.data[index]['date']][joint]['max'], care_plan_serializer.data[index]['output_json'][time][exercise]['rom'][joint]['max'])
                        temp = {}
                        temp_3 = {}
                        temp_4 = {}
                        temp_5 = {}
                        temp_6 = {}
                        temp = {}
                        temp['Joints'] = joint
                        temp['max'] = care_plan_serializer.data[index]['output_json'][time][exercise]['rom'][joint]['max']   
                        temp['min'] = care_plan_serializer.data[index]['output_json'][time][exercise]['rom'][joint]['min'] 
                        temp['time_slot'] = str(time)
                        temp['exercise_name'] = str(exercise) 
                        temp["MaxColor"] = "hsl(18, 70%, 50%)"
                        temp["MinColor"] = "hsl(18, 70%, 50%)"
                       # temp_3['exercise'] = str(exercise)
                       # temp_4['exercise'] = str(exercise)
                       # temp_5['exercise'] = str(exercise)
                       # temp_6['exercise'] = str(exercise)
                        for j in care_plan_serializer.data[index]['exercise_details']:
                           
                            if j['name'] == exercise:
                                temp_3['y'] = j['Rom']['max']
                                temp_3['x'] = care_plan_serializer.data[index]['date']
                                temp_4['y'] = j['Rom']['min']
                                temp_4['x'] = care_plan_serializer.data[index]['date']
                                temp_5['x'] = care_plan_serializer.data[index]['date']
                                temp_5['y'] = care_plan_serializer.data[index]['output_json'][time][exercise]['rom'][j['Rom']['joint']]['max']
                                temp_6['x'] = care_plan_serializer.data[index]['date']
                                temp_6['y'] = care_plan_serializer.data[index]['output_json'][time][exercise]['rom'][j['Rom']['joint']]['min']
                        response['data_vertical_bar'].append(temp)
                    target_max['data'].append(temp_3)
                    target_min['data'].append(temp_4)
                    current_max['data'].append(temp_5)
                    current_min['data'].append(temp_6)    

            response['data_vertical_bar2'].append(temp_2)
            response['data_line'].append(target_max)
            response['data_line'].append(target_min)
            response['data_line'].append(current_max)
            response['data_line'].append(current_min)
            response['new_data'] = new_data
            response['score'] = (exercise_done/total_exercise)*100
            response['compliance'][care_plan_serializer.data[index]['date']] = ((today_total - today_done)/today_total)*100
           

    except Exception as e:
   #     print(e)
        pass

    return Response(response)


@csrf_exempt
@api_view(['POST'])
def basic_detail(request):
    db = myclient['Darwin']
    db = db['pp_episode_detail']
    try:   
        response = {}
        patient = pp_patient_master.objects.filter(pp_patm_id = request.data['id']).first()
        patient = pp_patient_master_masterSerializer(patient)    
        for i in patient.data.keys(): 
            response[str(i)] = patient.data[i] 
        
    

        epi = db.find({"pp_pm_id":patient.data['pp_patm_id']}).sort([("pp_ed_id",-1)])
        
        if epi.count()>0:
            epi = epi[0]
            del epi['_id']
            response['pp_ed_id'] = epi['pp_ed_id']
            response['episode_code'] = epi['episode_number']
            response['primary_complaint'] = epi['primary_complaint']
            response['Operative_Types'] = epi['Operative_Types']
            response['start_date'] = epi['start_date']

        return Response(response)
    except Exception as e:
        
       
        return Response(status=status.HTTP_400_BAD_REQUEST)    
 






from django.http import HttpResponse
import mimetypes
@csrf_exempt
@api_view(['GET'])
def file_download(request,slug):
    f1_path = "/home/ec2-user/uploadedfiles/"+slug
    
    filename = slug
    f1 = open(f1_path,'rb')
    mime_type, _ = mimetypes.guess_type(f1_path)
    response = HttpResponse(f1, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
