from django.db import models

# Create your models here.



class ex_exercise_master(models.Model):

    ex_em_id                 = models.AutoField(primary_key = True)
    exercise_shortname       = models.CharField( max_length=20)
    title                    = models.CharField(max_length=200)
    image_path               = models.CharField( max_length=700,blank = True,null = True, default=None)
    video_path               = models.CharField( max_length=700,blank = True,null = True, default=None)
    difficulty_level         = models.CharField( max_length=15)
    age_group                = models.IntegerField(blank = True,null = True, default=None)
    assistance               = models.CharField( max_length=300,blank = True,null = True, default=None)
    aim                      = models.CharField( max_length=300,blank = True,null = True, default=None)
    instruction1             = models.CharField( max_length=1000,blank = True,null = True, default=None)
    instruction2             = models.CharField( max_length=1000,blank = True)
    status                   = models.IntegerField()
    flex_field_1             = models.CharField( max_length=200,blank = True,null = True, default=None)
    flex_field_2             = models.CharField( max_length=200,blank = True,null = True, default=None)
    flex_field_3             = models.CharField( max_length=200,blank = True,null = True, default=None)
    flex_field_4             = models.CharField( max_length=200,blank = True,null = True, default=None)
    flex_field_5             = models.CharField( max_length=200,blank = True,null = True, default=None)
    search_tags              = models.CharField( max_length=500,blank = True,null = True, default=None)


    class Meta:
        db_table='ex_exercise_master'


    def __str__(self):
        return self.title
        


class ex_exercise_instructions(models.Model):

    ex_ei_id        =  models.AutoField(primary_key = True)
    ex_em_id        = models.ForeignKey(ex_exercise_master, on_delete=models.CASCADE)
    language_code   = models.CharField( max_length=50)
    instructions    = models.CharField( max_length=500)

    class Meta:
        db_table  = 'ex_exercise_instructions'



class Ex_ExerciseTemplates_master(models.Model):
    ex_extmp_id       = models.AutoField(primary_key = True)       
    template_desc     = models.CharField( max_length=1000)
    ex_em_id          = models.ForeignKey(ex_exercise_master, on_delete=models.CASCADE)
    sets              = models.IntegerField(blank = True,null = True, default=None)
    status            = models.IntegerField(blank = True,null = True, default=None)
    flex_field_1      = models.CharField( max_length=200)
    flex_field_2      = models.CharField( max_length=200)

    class Meta:
        db_table = 'Ex_ExerciseTemplates_master'





class ex_joint_master(models.Model):
    ex_jm_id             = models.AutoField(primary_key = True)
    joint_name           = models.CharField( max_length=100)
    status               = models.IntegerField()
    model_name           = models.CharField( max_length=200)
    flex_field_1         = models.CharField( max_length=200,blank = True,null = True, default=None)
    flex_field_2         = models.CharField( max_length=200,blank = True,null = True, default=None)
    flex_field_3         = models.IntegerField(blank = True,null = True, default=None)
    flex_field_4         = models.IntegerField(blank = True,null = True, default=None)


    def __str__(self):
        return self.joint_name
    


class ex_movement_master(models.Model):
    ex_mov_id          = models.AutoField(primary_key = True)
    moment_direction   = models.CharField( max_length=300)
    pp_plan_id         = models.IntegerField()
    flex_field_2       = models.CharField( max_length=200,blank = True,null = True, default=None)
    flex_field_3       = models.IntegerField(blank = True,null = True, default=None)


    def __str__(self):
        return self.moment_direction
    


class ex_muscles_master(models.Model):
    ex_mus_id           = models.AutoField(primary_key = True)    
    muscle_name         = models.CharField( max_length=200)
    status              = models.IntegerField()
    flex_field_1         = models.CharField( max_length=200,blank = True,null = True, default=None)
    flex_field_2         = models.CharField( max_length=200,blank = True,null = True, default=None)
    flex_field_3         = models.IntegerField(blank = True,null = True, default=None)
    flex_field_4         = models.IntegerField(blank = True,null = True, default=None)


    def __str__(self):
        return self.muscle_name
    

class ex_excercise_joints_mapping(models.Model):
    ex_ejm_id             = models.AutoField(primary_key = True)
    ex_em_id              = models.ForeignKey(ex_exercise_master, on_delete=models.CASCADE)
    ex_jm_id              = models.ForeignKey(ex_joint_master,  on_delete=models.CASCADE)
    max_angle             = models.IntegerField()
    min_angle             = models.IntegerField()
    joint_priority        = models.IntegerField(blank = True,null = True, default=None)
    status                = models.IntegerField()
    flex_field_1         = models.IntegerField( blank = True,null = True, default=None)
    flex_field_2         = models.IntegerField(blank = True,null = True, default=None)
    flex_field_3         = models.CharField( max_length=200,blank = True,null = True, default=None)

class ex_excercise_movement_mapping(models.Model):
    ex_emm_id           = models.AutoField(primary_key = True)
    ex_mov_id           = models.ForeignKey(ex_movement_master, on_delete=models.CASCADE)
    ex_em_id            = models.ForeignKey(ex_exercise_master, on_delete=models.CASCADE)
    ex_plane_id         = models.IntegerField(blank = True,null = True, default=None)
    status              = models.IntegerField()
    flex_field_1         = models.IntegerField(blank = True,null = True, default=None)
    flex_field_2         = models.CharField( max_length=200,blank = True,null = True, default=None)


class ex_excercise_muscle_mapping(models.Model):
    ex_exmus_id      = models.AutoField(primary_key =True)
    ex_mus_id        = models.ForeignKey(ex_muscles_master, on_delete=models.CASCADE)
    ex_em_id            = models.ForeignKey(ex_exercise_master, on_delete=models.CASCADE)
    ex_plane_id         = models.IntegerField(blank = True,null = True, default=None)
    status              = models.IntegerField()
    flex_field_1         = models.IntegerField(blank = True,null = True, default=None)
    flex_field_2         = models.CharField( max_length=200,blank = True,null = True, default=None)





class ex_care_plan(models.Model):
    pp_cp_id          = models.AutoField(primary_key = True)
    careplan_code     = models.CharField( max_length=50)
    episode_id        = models.IntegerField(blank = True,null = True, default=None)
    start_date        = models.DateField(blank = True,null = True, default=None)
    end_date        = models.DateField(blank = True,null = True, default=None)
    exercise_details  = models.JSONField(blank = True,null = True, default=None)
    time_slot         = models.JSONField(blank = True,null = True, default=None)
    date              = models.DateField(blank = True,null = True, default=None)
    status            = models.CharField(max_length=50,blank = True,null = True, default=None)
    status_flag       = models.IntegerField()
    output_json       = models.JSONField(blank = True,null = True, default=None)
    creation_date     = models.DateField(auto_now_add=True)
    created_by        = models.IntegerField(blank = True,null = True, default=None)
    last_update_date  = models.DateField(auto_now_add=True)
    last_updated_by   = models.IntegerField(blank = True,null = True, default=None)



class jointIndex(models.Model):
    joint = models.ForeignKey(ex_joint_master , on_delete=models.CASCADE,related_name = 'index')
    index = models.IntegerField()
