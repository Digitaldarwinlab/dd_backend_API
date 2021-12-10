from Auth.models import User,Admin_info,register_user
from rest_framework import serializers
import re

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=6,write_only=True,required=True)

    

    class Meta:
        model = User
        fields = ['email','password','uid','is_patient']

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)    

    # def validate_password(self,value):
    #     reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    #     if not re.search(reg, value):
    #         raise serializers.ValidationError("please enter strong password")
    #     return value    


class emaiSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class ResetPassSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']


class AdminInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin_info
        fields = '__all__'          




class register_userSerializer(serializers.ModelSerializer):
    class Meta:
        model = register_user
        fields = '__all__'                
