from rest_framework import serializers
from episode.models import pp_episode_detail,pp_prescription_detail,pp_visit_detail,pp_assessment_detail,pp_questionnaire_template,pp_notes



class pp_episode_detailSerializer(serializers.ModelSerializer):

    class Meta:
        model = pp_episode_detail
        fields = '__all__'


class pp_prescription_detailSerializer(serializers.ModelSerializer):

    class Meta:
        model = pp_prescription_detail
        fields = '__all__'


class pp_visit_detailSerializer(serializers.ModelSerializer):

    class Meta:
        model = pp_visit_detail
        fields = '__all__'



class pp_assessment_detailSerializer(serializers.ModelSerializer):

    class Meta:
        model = pp_assessment_detail
        fields = '__all__'


class pp_questionnaire_templateSerializer(serializers.ModelSerializer):

    class Meta: 
        model = pp_questionnaire_template
        fields = '__all__'

class pp_notesSerializer(serializers.ModelSerializer):

    class Meta: 
        model = pp_notes
        fields = '__all__'