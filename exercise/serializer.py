from rest_framework import serializers
from exercise.models import ex_exercise_master,ex_joint_master,ex_movement_master,ex_muscles_master,ex_excercise_joints_mapping,ex_excercise_movement_mapping,ex_excercise_muscle_mapping,ex_exercise_instructions,Ex_ExerciseTemplates_master,ex_care_plan,jointIndex


class ex_exercise_master_masterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ex_exercise_master
        fields = '__all__'


class jointIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = jointIndex
        fields = ['index']





        
class ex_joint_masterSerializer(serializers.ModelSerializer):
    index = jointIndexSerializer(many = True,read_only=True)
    class Meta:
        model = ex_joint_master
        fields = ['ex_jm_id','joint_name','status','model_name','flex_field_1','flex_field_2','flex_field_3','flex_field_4','index']

class ex_movement_masterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ex_movement_master
        fields = '__all__'

class ex_muscles_masterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ex_muscles_master
        fields = '__all__'

class ex_excercise_joints_mappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ex_excercise_joints_mapping
        fields = '__all__'

class ex_excercise_muscle_mappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ex_excercise_muscle_mapping
        fields = '__all__'
class ex_excercise_movement_mappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ex_excercise_movement_mapping
        fields = '__all__'

class ex_exercise_instructionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ex_exercise_instructions
        fields = '__all__'

class Ex_ExerciseTemplates_masterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ex_ExerciseTemplates_master
        fields = '__all__'

class ex_care_planSerializer(serializers.ModelSerializer):
    class Meta:
        model = ex_care_plan
        fields = '__all__'


