from rest_framework import serializers

from patient.models import pp_patient_master
import re

class pp_patient_master_masterSerializer(serializers.ModelSerializer):
    class Meta:
        model = pp_patient_master
        fields = '__all__'

    def validate_first_name(self,value):

         if  re.search("^[a-zA-Z]+$", value):
           return value
            
         raise serializers.ValidationError("state name should only contain characters ")

 
    def validate_middle_name(self,value):

         if  re.search("^[a-z A-Z]+$", value):
           return value
            
         raise serializers.ValidationError("state name should only contain characters ")

 
    def validate_last_name(self,value):

          if  re.search("^[a-zA-Z]+$", value):
           return value
            
          raise serializers.ValidationError("state name should only contain characters ")


    def validate_pin(self,value):

        if  len(str(value))!=6:
            raise serializers.ValidationError("incorrect pin ")
            
        return value





    def validate_blood_group(self,value):
        bg = ['A+','A-','B+','B-','O+','O-','AB+','AB-','A','B','O','AB']

        if  value not in bg:
            raise serializers.ValidationError("invalide blood group ")
        return value



    def validate_mobile_no(self,value):
       

        if  re.search("^[0-9]{10,12}$", value):
            return value
        raise serializers.ValidationError("invalide mobile number")



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
         

 

        

