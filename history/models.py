from django.db import models
from Auth.models import User,UserManager
#from phone_field import PhoneField
from Auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinLengthValidator
from django.core.validators import MaxValueValidator

# Create your models here.



class pp_physiotherapist_history(models.Model):
    history_id        = models.AutoField(primary_key = True)
    pp_pm_id          = models.IntegerField()
    first_name        = models.CharField( max_length=50)
    middle_name       = models.CharField( max_length=50,blank=True)
    last_name         = models.CharField( max_length=50)
    physio_code       = models.CharField( max_length=50,blank=True, null=True, default=None)
    Doctor_type       = models.IntegerField()
    Address_1         = models.CharField( max_length=150)
    Address_2         = models.CharField( max_length=150,blank=True)
    Address_3         = models.CharField( max_length=150,blank=True)
    gender            = models.CharField( max_length=10,blank = True)
    city              = models.CharField( max_length=50)
    state             = models.CharField( max_length=50)
    country           = models.CharField( max_length=50)
    mobile_no         = models.CharField( max_length=15)
    whatsapp_no       = models.CharField( max_length=12)
    landline          = models.CharField( max_length=12,blank = True)
    facebook          = models.CharField( max_length=50, blank=True, null=True, default=None)
    linkedin          = models.CharField( max_length=50, blank=True, null=True, default=None)
    regd_no_1         = models.CharField(max_length=50,unique = True)
    regd_no_2         = models.CharField(max_length=50, blank=True, null=True, default=None)
    degree            = models.CharField( max_length=12)
    expertise_1       = models.CharField( max_length=50)
    expertise_2       = models.CharField( max_length=50,blank=True)
    expertise_3       = models.CharField( max_length=50,blank=True)
    start_date        = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_date          = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True)
    status_flag       = models.IntegerField()
    roleId            = models.IntegerField()
    updated_at        = models.DateField( auto_now_add=True)
    updated_by        = models.CharField(max_length=50)


    class Meta:
        db_table='pp_physiotherapist_history'


class pp_patient_history(models.Model):
    history_id               = models.AutoField(primary_key = True)
    pp_patm_id               = models.IntegerField()
    pp_pm                    = models.IntegerField()
    first_name               = models.CharField( max_length=50,validators=[MinLengthValidator(3)])
    middle_name              = models.CharField( max_length=50,blank = True,  null=True, default=None)
    last_name                = models.CharField( max_length=50,validators=[MinLengthValidator(3)])
    dob                      = models.DateField( auto_now=False, auto_now_add=False)
    patient_code             = models.CharField(max_length=50,blank=True, null=True, default=None)
    Address_1                = models.CharField( max_length=150)
    Address_2                = models.CharField( max_length=150,blank=True)
    Address_3                = models.CharField( max_length=150,blank=True)
    city                     = models.CharField( max_length=50)
    state                    = models.CharField( max_length=50)
    country                  = models.CharField( max_length=50)
    pin                      = models.CharField(max_length=50)
    gender                   = models.CharField(max_length=10,blank = True)
    mobile_no                = models.CharField( max_length=12)
    whatsapp_no              = models.CharField( max_length=12)
    landline                 = models.CharField( max_length=12,blank=True)
    email                    = models.CharField(max_length=50)
    facebook                 = models.CharField( max_length=200,blank=True, null=True, default=None)
    linkedlin                = models.CharField( max_length=200,blank=True, null=True, default=None)
    emergence_contact        = models.CharField(max_length=50)
    blood_group              = models.CharField( max_length=4)
    allergy_detail           = models.CharField( max_length=200,blank=True, null=True, default=None)
    patient_medical_history  = models.CharField( max_length=1000,blank=True, null=True, default=None)
    patient_Family_History   = models.CharField( max_length=1000,blank=True, null=True, default=None)
    status_flag              = models.CharField(max_length=50)
    last_update_date         = models.CharField( max_length=50)
    last_update_by           = models.CharField(max_length=50)
    updated_at               = models.CharField(max_length=50)
    updated_by               = models.CharField(max_length=50)

    class Meta:
        db_table='pp_patient_history'




class pp_episode_history(models.Model):
    pp_ed_id                    = models.IntegerField()
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
    updated_at                  = models.CharField(max_length=50)
    updated_by                 = models.CharField(max_length=50)


    class Meta:
        db_table='pp_episode_history'

# Create your models here.
