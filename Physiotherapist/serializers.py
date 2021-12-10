from rest_framework import serializers
from Physiotherapist.models import pp_physiotherapist_master,pp_otp,old_password,pp_code
import re


class pp_physiotherapist_masterSerializer(serializers.ModelSerializer):
    class Meta:
        model = pp_physiotherapist_master
        fields = '__all__'
        
    def validate_first_name(self,value):

        if  re.search("^[a-zA-Z]+$", value):
           return value
            
        raise serializers.ValidationError("first name should only contain characters ")

 
    def validate_middle_name(self,value):

       if  re.search("^[a-zA-Z]+$", value):
           return value
            
       raise serializers.ValidationError("middle name should only contain characters ")
 
    def validate_last_name(self,value):

        if  re.search("^[a-zA-Z]+$", value):
           return value
            
        raise serializers.ValidationError("last name should only contain characters ")


    def validate_degree(self,value):

        if  re.search("[1-9~!@#$%^&*()+=]", value):
           raise serializers.ValidationError("degree name should only contain characters ")
 
           
            
        return value



    def validate_country(self,value):

         if  re.search("^[a-z A-Z]+$", value):
           return value
            
         raise serializers.ValidationError("country name should only contain characters ")






    def validate_state(self,value):

         if  re.search("^[a-z A-Z]+$", value):
           return value
            
         raise serializers.ValidationError("state name should only contain characters ")


 
    def validate_city(self,value):

        if  re.search("^[a-z A-Z]+$", value):
           return value
            
        raise serializers.ValidationError("city name should only contain characters ")
 


class pp_otpSerializer(serializers.ModelSerializer):
    class Meta:
        model = pp_otp
        fields = '__all__'



class mobileSerilizer(serializers.ModelSerializer):

    class Meta:
        model = pp_physiotherapist_master
        fields = ['mobile_no']         

class old_password_serializer(serializers.ModelSerializer):

    class Meta:
        model  = old_password
        fields  = '__all__'








class pp_codeserializer(serializers.ModelSerializer):

    class Meta:
        model  = pp_code
        fields  = '__all__'

