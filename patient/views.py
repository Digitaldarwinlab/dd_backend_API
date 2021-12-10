from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view , schema
from patient.models import pp_patient_master
from patient.serializer import pp_patient_master_masterSerializer
from Physiotherapist.models import pp_physiotherapist_master,pp_code,pp_otp
from Physiotherapist.serializers import pp_codeserializer,pp_otpSerializer,pp_physiotherapist_masterSerializer
from Auth.models import User
from Auth.serializer import UserSerializer
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status
import jwt , datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.mail import send_mail
from history.models import pp_patient_history
from history.serializer import pp_patient_history_serializer
import pymongo
import logging
logger = logging.getLogger("info")
myclient = pymongo.MongoClient("mongodb://172.31.0.49:27017")


token_param_config = openapi.Parameter('name',in_ = openapi.IN_QUERY,description = 'Description',type = openapi.TYPE_STRING)
user_response = openapi.Response('response description', {'message':'created'})
@csrf_exempt
@swagger_auto_schema(manual_parameters = [token_param_config],methods=['post'],request_body=pp_patient_master_masterSerializer)
@api_view(['POST'])
def patient_reg(request):
    
    duplicate = pp_patient_master.objects.filter(first_name = request.data['first_name'],dob = request.data['dob'])
    if duplicate:
        print(duplicate)
        return Response({"message":"User with same first name and date of birth already exist"})
    
    temp = pp_patient_master.objects.all().order_by('-pp_patm_id')
    
    
    codes = pp_code.objects.filter(prefix = 'P')
    code = pp_codeserializer(codes,many = True)
    count = 0
    for i in range(0,len(code.data[0]['code'])):
        if code.data[0]['code'][i] == '9':
            count+=1         

    
    patient_code = 'P.' + request.data['first_name'][0:3] + request.data['last_name'][0:3] + code.data[0]['code']

    if code.data[0]['length'] ==count:
        if code.data[0]['code'][5-code.data[0]['length']]!= 'Z':
            c = ord(code.data[0]['code'][5-code.data[0]['length']])
            code.data[0]['code'] = str(chr(c+1)) + '1' + str('0'*(code.data[0]['length']-1)) 

    else:
        code.data[0]['code'] = str(int(code.data[0]['code'][5-code.data[0]['length']:])+1)
        
        serializer = pp_codeserializer(codes[0],data = code.data[0],partial = True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)          


    request.data['patient_code'] = patient_code
    data = request.data
    login_data = {}
    login_data['email'] = request.data['email']
    login_data['uid'] = patient_code[2:]
    password = generate_password()
    login_data['password'] = password
    login_data['is_patient'] = True
    user_serializer = UserSerializer(data = login_data)
    if not user_serializer.is_valid():
        return Response(serializer.errors)
    user_serializer.save()    

    send_mail('email varification',
    'your password is '+password +' and uid is '+patient_code[2:],'mishra.satwik9532@gmail.com',[login_data['email']],fail_silently=False)
        
  #  data['pp_pm'] = payload['id']
    
    data['last_update_date'] = datetime.datetime.utcnow()
    data['last_update_by'] = datetime.datetime.utcnow()
    data['status_flag'] =2
    serializer = pp_patient_master_masterSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message':'patient added','role':'patient'},status=status.HTTP_201_CREATED)
    data = User.objects.filter(email=login_data['uid'])
    data.delete()
      
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)   




@csrf_exempt
@api_view(['POST'])
def get_patient(request):
    # if not request.COOKIES.get('jwt'):
    #     raise exceptions.AuthenticationFailed('unauthenticated')
    # token = request.COOKIES.get('jwt')
    # try:
    #     payload = jwt.decode(token,'secret_key',algorithms=['HS256'])  

    # except jwt.ExpiredSignatureError:
    #    raise exceptions.AuthenticationFailed('unauthenticated')
    log_info = {}
    try:
        log_info['tran'] = request.COOKIES['tran']
    except:
        pass
    log_info['request_body'] = request.data
    check = User.objects.filter(pk = request.data['id']).first()
    if check.is_staff:
     
        data = pp_patient_master.objects.all().order_by('-pp_patm_id')
        lens = data.count()
        data = pp_patient_master_masterSerializer(data,many = True)

        for i in range(0,lens):
            if type(data.data[i]['patient_code']) == str:
                data.data[i]['uid'] = data.data[i]['patient_code'][2:]
        log_info['reponse_body'] = data.data      
        logger.info(log_info)        
        return Response(data.data,status=status.HTTP_200_OK)


    data =  pp_patient_master.objects.filter(pp_pm = request.data['id']).order_by('-pp_patm_id')
    serializer = pp_patient_master_masterSerializer(data,many =True)
    if type(serializer.data[0]['patient_code']) == str:
        serializer.data[0]['uid'] = serializer.data[0]['patient_code'][2:]
    log_info['reponse_body'] = serializer.data    
    logger.info(log_info)     
    return Response(serializer.data,status=status.HTTP_200_OK)

    
@csrf_exempt
@api_view(['GET','POST'])

def search(request):
    db = myclient['Darwin']
    db = db['pp_episode_detail']
    try:
        query = pp_patient_master.objects.filter(first_name__icontains = request.data['query']) | pp_patient_master.objects.filter(last_name__icontains = request.data['query']) | pp_patient_master.        objects.filter(mobile_no__icontains = request.data['query'])| pp_patient_master.objects.filter(patient_code__icontains = request.data['query'])
    
        if query.count()>0:
            user = User.objects.filter(pk = request.data['id']).first()
            if user.is_superuser:
                serializer = pp_patient_master_masterSerializer(query,many = True)

                for i in range(0,query.count()):
                    if type(serializer.data[i]['patient_code']) == str:
                        serializer.data[i]['uid'] = serializer.data[i]['patient_code'][2:]
                    episode_datail = db.find({"pp_pm_id":serializer.data[i]['pp_patm_id']}).sort([("pp_ed_id",-1)]) 
                 
                    if episode_datail.count()>0 and 'end_date' in episode_datail[0] and len(episode_datail[0]['end_date'])<1:
                        
                        serializer.data[i]['pp_ed_id'] = episode_datail[0]['pp_ed_id']
                    else:
                        serializer.data[i]['pp_ed_id'] = None    
            
                return Response(serializer.data,status = status.HTTP_200_OK) 

            else:
                query = query.filter(pp_pm= request.data['id'])
                serializer = pp_patient_master_masterSerializer(query,many = True)
                for i in range(0,query.count()):
                    if type(serializer.data[i]['patient_code']) == str: 
                        serializer.data[i]['uid'] = serializer.data[i]['patient_code'][2:]
                    episode_datail = db.find({"pp_pm_id":serializer.data[i]['pp_patm_id']}).sort([("pp_ed_id",-1)])

                    if episode_datail.count()>0 and 'end_date' in episode_datail[0] and len(episode_datail[0]['end_date'])<1:

                        serializer.data[i]['pp_ed_id'] = episode_datail[0]['pp_ed_id']
                    else:
                        serializer.data[i]['pp_ed_id'] = None
                
                return Response(serializer.data,status = status.HTTP_200_OK)    
        return Response(status=status.HTTP_404_NOT_FOUND)   

    except:
        return Response(status = status.HTTP_400_BAD_REQUEST)     
 


 
from django.http import JsonResponse
@csrf_exempt
def error_500(request):
    return JsonResponse({"message": "internal server error"}, status=500)

@csrf_exempt    
def error_404(request, exception):
    return JsonResponse({"message": "invalide API"}, status=404)



@csrf_exempt
@api_view(['POST'])
def validate_email(request):

    try:

        if User.objects.filter(email = request.data['email']).exists():
            return Response({'message':'email already exists'},status = status.HTTP_409_CONFLICT)

        else:
            return Response(status = status.HTTP_200_OK)     
    except:
        return Response(status = status.HTTP_400_BAD_REQUEST)            




        
@csrf_exempt
@api_view(['POST'])
def validate_mobile(request):

    try:
        if pp_patient_master.objects.filter(mobile_no = request.data['mobile_no']).exists():
            return Response({'message':'mobile number already exists'},status = status.HTTP_409_CONFLICT)

        else:
            return Response(status = status.HTTP_200_OK)    
    except:
        return Response(status = status.HTTP_400_BAD_REQUEST)            


@csrf_exempt
@api_view(['POST'])
def update_patient(request):
    data = pp_patient_master.objects.filter(pp_patm_id=request.data['id']).first() 
    serializer = pp_patient_master_masterSerializer(data)
    data_for_update_table = serializer.data
    data_for_update_table["updated_at"] = str(datetime.date.today())

    data_for_update_table['updated_by'] = get_ip(request)
    update_seialize = pp_patient_history_serializer(data = data_for_update_table)
    serializer = pp_patient_master_masterSerializer(data,data=request.data,partial=True)
    if serializer.is_valid():
        if update_seialize.is_valid():
            update_seialize.save()
        else:
            return Response(update_seialize.errors) 
        serializer.save()
        return Response({'message':'data updated','error':False},status=status.HTTP_200_OK)  

    return Response(serializer.errors)    




import random as r
import array
def generate_password():
    MAX_LEN = 8
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                     'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                     'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                     'z']

    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                     'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
                     'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                     'Z']                 
    SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
           '*', '(', ')', '<']

    COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS
    rand_digit = r.choice(DIGITS)
    rand_upper = r.choice(UPCASE_CHARACTERS)
    rand_lower = r.choice(LOCASE_CHARACTERS)
          
    temp_pass = rand_digit + rand_upper + rand_lower 
    for x in range(MAX_LEN - 4):
        temp_pass = temp_pass + r.choice(COMBINED_LIST)
 
    # convert temporary password into array and shuffle to
    # prevent it from having a consistent pattern
    # where the beginning of the password is predictable
        temp_pass_list = array.array('u', temp_pass)
        r.shuffle(temp_pass_list)
    password = ""
    for x in temp_pass_list:
        password = password + x        

    return password                







@csrf_exempt
@api_view(['POST','GET'])
def patient_profile(request,id = None):
    if request.method == "POST":

        try:
            profile = pp_patient_master.objects.filter(pp_patm_id = request.data['id']).first()
            serializer = pp_patient_master_masterSerializer(profile)
            return Response(serializer.data)
        except:
            return  Response(status = status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        try:
            profile = pp_patient_master.objects.filter(pp_patm_id = id).first()
            serializer = pp_patient_master_masterSerializer(profile)
            return Response(serializer.data)
        except:
            return  Response(status = status.HTTP_400_BAD_REQUEST)







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


