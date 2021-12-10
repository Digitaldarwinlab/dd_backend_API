from clinic.models import pp_clinic_master
from rest_framework import serializers

class pp_clinic_masterSerializer(serializers.ModelSerializer):

    class Meta:
        model = pp_clinic_master
        fields = '__all__'
