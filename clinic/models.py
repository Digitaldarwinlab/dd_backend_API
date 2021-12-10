from django.db import models

# Create your models here.

class pp_clinic_master(models.Model):

    pp_cm_id           = models.AutoField(primary_key = True)
    clinic_code        = models.CharField(max_length=50,blank=True, null=True, default=None)
    name               = models.CharField( max_length=50)
    address_1          = models.CharField(max_length=200)
    address_2          = models.CharField(max_length=200,blank=True, null=True, default=None)
    address_3          = models.CharField(max_length=200,blank=True, null=True, default=None)
    city               = models.CharField(max_length=50,blank=True, null=True, default=None)
    state              = models.CharField(max_length=50)
    country            = models.CharField(max_length=50)
    zip                = models.PositiveIntegerField()
    estab_date         = models.DateField()
    mobile_no          = models.CharField( max_length=15)
    landline_no        = models.CharField( max_length=15,blank=True, null=True, default=None)
    mobile_no          = models.CharField( max_length=15)
    email              = models.EmailField( max_length=254,unique = True)
    website_url        = models.URLField( max_length=200,blank=True, null=True, default=None)
    digital_clinic     = models.IntegerField(blank=True, null=True, default=None)
    start_date         = models.DateField()
    end_date           = models.DateField(blank=True, null=True, default=None)
    status_flag        = models.IntegerField(blank=True, null=True, default=None)
    last_update_date   = models.DateField(auto_now_add=True)
    last_update_by     = models.CharField( max_length=50)


    class Meta:
        db_table = 'pp_clinic_master'


    def __str__(self):
        return self.email
