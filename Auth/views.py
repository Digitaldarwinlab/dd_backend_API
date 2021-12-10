from django.shortcuts import render
from Auth.models import User,register_user
from Auth.serializer import register_userSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view,schema
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
# @csrf_exempt
# @api_view(['POST'])
# def password_reset(request):

#     if User.objects.filter(email = request.data['email']):
#         user = User.objects.get(email = request.data['email'])
#         uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
#         token = PasswordResetTokenGenerator().make_token(user)
#         current_site = get_current_site(request=request).domain
#         relativeLink = reverse( kwargs={'uidb64': uidb64, 'token': token})
#         redirect_url = request.data.get('redirect_url', '')
#         absurl = 'http://'+current_site + relativeLink
#         email_body = 'Hello, \n Use link below to reset your password  \n' + \
#                 absurl+"?redirect_url="+redirect_url
#         data = {'email_body': email_body, 'to_email': user.email,
#                 'email_subject': 'Reset your passsword'}
#         Util.send_email(data)
#     return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)




import jwt
@csrf_exempt
@api_view(['POST'])
def password_change_request(request):
    if User.objects.filter(uid = request.data['uid']).exists():
        user = User.objects.get(uid = request.data['uid'])
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))

        payload = {'uid':user.uid} 
        token =  jwt.encode(payload,'secret_key',algorithm='HS256')

        url = 'https://myphysio.digitaldarwin.in/password_reset/'+token
        send_mail('password Reset',
        'click on this link '+url,'mishra.satwik9532@gmail.com',[user.email],fail_silently=False)
        return Response({"message":"check your email for further process"},status = status.HTTP_200_OK)
    return Response({"message":"uid not exist"},status=status.HTTP_404_NOT_FOUND)    


@csrf_exempt
@api_view(['POST'])
def reset_password_confirm(request):
  
    if 'token' in request.data:
        
        token = request.data['token']
        payload = jwt.decode(token,'secret_key',algorithms=['HS256'])
        user = User.objects.get(uid = payload['uid'])
        user.set_password (request.data['new_password'])
        user.save()
        return Response({"messge":"password change successfully"})
    return Response({"message":"please provide token"})    








import re
def validated_password(password):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pat = re.compile(reg)
    mat = re.search(pat, password)

    if mat:
        return True
    else:
        return False    









@csrf_exempt
@api_view(['POST'])
def admin_password_reset(request):
    
    if validated_password(request.data['new_password']) == False:
        return Response({"message":"password is too weak"},status=status.HTTP_400_BAD_REQUEST)      
    
    user = User.objects.filter(id=request.data['id']).first()  
    if user.is_superuser:
       
        user_to_change = User.objects.filter(uid = request.data['uid']).first()
        user_to_change.set_password(request.data['new_password'])
        user_to_change.save()
        send_mail('email change',
        'your new password is '+request.data['new_password'] ,'mishra.satwik9532@gmail.com',[user_to_change.email],fail_silently=False)
    else:
        return Response({"message": "sorry you are not a adminyy"})    
    
    
    return Response({'message':'password change succesfully'},status = status.HTTP_200_OK)








@csrf_exempt
@api_view(['POST'])
def add_register_user(request):

    try:
        serializer = register_userSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":'user register'},status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)    

    except :
        return Response(status=status.HTTP_400_BAD_REQUEST)       


monthDict={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
from datetime import date,timedelta
import calendar
@csrf_exempt
@api_view(['GET'])
def get_calendar(request):
    try:
        id = int(request.GET.get("id"))
    except:
        id = 0
        pass
    result = []
    today_date = date.today()
    temp = {}
    temp['date'] = str(today_date)
    temp['displayDay'] = str(today_date)[-2:]
    temp['displayMonth'] = monthDict[int(str(today_date)[5:7])]
   # print(today_date[5:7])
    temp['displayYear'] = str(today_date)[:4]
    temp['dayName'] = calendar.day_name[today_date.weekday()]
    day_no = today_date.weekday()
    result.append(temp)
    if id>=0:
        for i in range(10*id+1,10*id+11):
            today_date = (date.today() + timedelta(days = i)).isoformat()
            temp = {}
            temp['date'] = str(today_date)
            temp['displayDay'] = str(today_date)[-2:]
            temp['displayMonth'] = monthDict[int(str(today_date)[5:7])]
            temp['displayYear'] = str(today_date)[:4]
            temp['dayName'] = calendar.day_name[(day_no + i)%7]
            result.append(temp)
        if id!=0:
            result.pop(0)
    else:
        for i in range(10*id+10,10*id-1,-1):
            
            today_date = (date.today() + timedelta(days = i)).isoformat()
                
            temp = {}
            temp['date'] = str(today_date)
            temp['displayDay'] = str(today_date)[-2:]
            temp['displayMonth'] = monthDict[int(str(today_date)[5:7])]
            temp['displayYear'] = str(today_date)[:4]
            temp['dayName'] = calendar.day_name[(day_no + i)%7]
            result.append(temp)
        if id!=0:
            result.pop(0)        

    return Response(result)    



# Create your views here.
