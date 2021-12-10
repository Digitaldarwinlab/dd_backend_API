from django.db import models
from django.core.validators import MinLengthValidator
from django.core.validators import MaxValueValidator
from Auth.models import User
# Create your models here.






class pp_patient_master(models.Model):
    pp_patm_id               = models.AutoField(primary_key=True)
    pp_pm                    = models.ForeignKey(User, on_delete=models.CASCADE)
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
    pin                      = models.PositiveIntegerField()
    gender                   = models.CharField(max_length=10,blank = True)
    mobile_no                = models.CharField( max_length=12)
    whatsapp_no              = models.CharField( max_length=12)
    landline                 = models.CharField( max_length=12,blank=True)
    email                    = models.EmailField( max_length=150)
    facebook                 = models.CharField( max_length=200,blank=True, null=True, default=None)
    linkedlin                = models.CharField( max_length=200,blank=True, null=True, default=None)
    emergence_contact        = models.BigIntegerField()
    blood_group              = models.CharField( max_length=4)
    allergy_detail           = models.CharField( max_length=200,blank=True, null=True, default=None)
    patient_medical_history  = models.CharField( max_length=1000,blank=True, null=True, default=None) 
    patient_Family_History  = models.CharField( max_length=1000,blank=True, null=True, default=None)
    status_flag              = models.IntegerField()
    last_update_date         = models.DateTimeField( auto_now=False, auto_now_add=False)
    last_update_by           = models.DateTimeField( auto_now=False, auto_now_add=False)
    
    class Meta:
        db_table='pp_patient_master'

