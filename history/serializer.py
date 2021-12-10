from rest_framework import serializers
from history.models import pp_patient_history,pp_physiotherapist_history,pp_episode_history

class pp_patient_history_serializer(serializers.ModelSerializer):
        
    class Meta:
        model = pp_patient_history
        fields = '__all__'



class pp_physiotherapist_history_serializer(serializers.ModelSerializer):

    class Meta:        
        model = pp_physiotherapist_history
        fields = '__all__'


class pp_episode_history_serializer(serializers.ModelSerializer):

    class Meta:        
        model = pp_episode_history
        fields = '__all__'


