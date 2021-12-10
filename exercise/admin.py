from django.contrib import admin
from exercise.models import ex_exercise_master,ex_joint_master,ex_movement_master,ex_muscles_master,ex_excercise_joints_mapping,ex_excercise_movement_mapping,ex_excercise_muscle_mapping,ex_exercise_instructions,Ex_ExerciseTemplates_master,ex_care_plan,jointIndex
# Register your models here.

admin.site.register(ex_exercise_master)
admin.site.register(ex_joint_master)
admin.site.register(ex_movement_master)
admin.site.register(ex_muscles_master)
admin.site.register(ex_excercise_joints_mapping)
admin.site.register(ex_excercise_movement_mapping)
admin.site.register(ex_excercise_muscle_mapping)
admin.site.register(Ex_ExerciseTemplates_master)
admin.site.register(ex_exercise_instructions)
admin.site.register(ex_care_plan)
admin.site.register(jointIndex)

