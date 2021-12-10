from django.db import models


#from django.contrib.postgres.fields import ArrayField


class pp_episode_detail(models.Model):
    pp_ed_id                    = models.AutoField(primary_key = True)
    episode_number              = models.CharField( max_length=200,blank=True, null=True, default=None)
    treating_doc_details        = models.CharField( max_length=200)
    PP_Patient_Details          = models.CharField( max_length=200)
    episode_start_date          = models.DateField(  auto_now_add=True)
    episode_end_date            = models.DateField( auto_now_add=True)
    operative_type              = models.CharField( max_length=50,blank=True, null=True, default=None)
    patient_history             = models.CharField( max_length=500,blank=True, null=True, default=None)
    attachment_required         = models.CharField( max_length=1000,blank=True, null=True, default=None)
    primary_complaint           = models.CharField( max_length=200)
    pp_ad_id                    = models.IntegerField(blank = True,null = True, default=None)
    Closure_notes               = models.CharField( max_length=1000,blank=True, null=True, default=None)
    final_assessment_date       = models.DateField(blank=True, null=True, default=None)
    pp_pm_id                    = models.IntegerField()
    status_flag                 = models.IntegerField(blank=True, null=True, default=None)
    
    
    class Meta:
        db_table='pp_episode_detail'




class pp_visit_detail(models.Model):
    pp_vd_id            = models.AutoField(primary_key = True)
   
    pp_ed_id            = models.IntegerField()
    visit_number        = models.IntegerField()
   
    appointment_detail   = models.JSONField()
    visit_type          = models.CharField( max_length=50)
    notes               = models.CharField( max_length=500,blank=True, null=True, default=None)
    status              = models.CharField( max_length=50)
    location            = models.CharField( max_length=50)
    creation_date       = models.DateField(auto_now_add=True)
    created_by          = models.DateField(auto_now_add = True)

    class Meta: 
        db_table = 'pp_visit_detail'


class pp_prescription_detail(models.Model):
    pp_pres_id            = models.AutoField(primary_key = True)
    pp_ed_id              = models.IntegerField()
    medication_detail     = models.JSONField( max_length=500,blank=True, null=True, default=None)
    lab_tests             = models.JSONField( max_length=500,blank=True, null=True, default=None)
    notes                 = models.CharField( max_length=500,blank=True, null=True, default=None)  

    class Meta:
        db_table = 'pp_prescription_detail'



class pp_assessment_detail(models.Model):
    pp_ad_id                  = models.AutoField(primary_key = True)
    pp_ed_id                  = models.IntegerField()
    assesmentdate             = models.DateField( auto_now_add=True)
    types                     = models.CharField( max_length=200)
    joint1score               = models.CharField( max_length=50)
    joint2score               = models.CharField( max_length=50)
    physical_assessement      = models.JSONField()
    questionnaires            = models.JSONField(blank=True, null=True, default=None)
    rom                       = models.JSONField(blank=True, null=True, default=None)
    class Meta:
        db_table = 'pp_assessment_detail' 


class pp_questionnaire_template(models.Model):
    pp_qt_id             = models.AutoField(primary_key = True)
    template_name        = models.CharField( max_length=50)
    description          = models.CharField( max_length=500,blank=True, null=True, default=None)
    question             = models.JSONField()
   
   

    class Meta:
        db_table = 'pp_questionnaire_template'


class pp_notes(models.Model):

    no_id              = models.AutoField(primary_key = True)
    eid                = models.IntegerField()
    notes              = models.JSONField()

    class Meta:
        db_table = 'pp_notes'







