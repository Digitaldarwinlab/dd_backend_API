from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,AbstractUser
# Create your models here.
from django.contrib.auth.models import PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError("User must have email")

        user =self.model(
            email=self.normalize_email(email),
            **extra_fields

        )   


        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,password,**extra_fields):


        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_active",True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuser must have is_staff-true')


        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must have is_superuser-true')


        return self.create_user(email, password,**extra_fields)


class User(AbstractUser):

    username            = None
    email               = models.EmailField(("email_address")) 
    first_name          =None
    last_name           =None
    uid                 = models.CharField(max_length=50,blank=True, null=True, default=None)
    is_patient          = models.BooleanField(blank=True, null=True, default=None)	
    
    
    USERNAME_FIELD   = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email
    

class Admin_info(models.Model):
    id             = models.OneToOneField(User , primary_key=True , on_delete=models.CASCADE)
    first_name     = models.CharField(max_length=50)
    middle_name    = models.CharField( max_length=50,blank = True)
    last_name      = models.CharField( max_length=50)        
    mobile_no      = models.CharField( max_length=15)
    whatsapp_no    = models.CharField( max_length=12)

    def __str__(self):
        return self.first_name
     




class register_user(models.Model):
    name                    = models.CharField(max_length=75)
    email                   = models.EmailField( max_length=254)
    mobile_no               = models.CharField(max_length=15)
    city                    = models.CharField( max_length=50)
    country                 = models.CharField( max_length=50)
    is_physio               = models.BooleanField(default=False) 
    is_enterprise           = models.BooleanField(default=False)   
    is_individual           = models.BooleanField(default=False)  
    organisation_name       = models.CharField( max_length=100, blank=True, null=True, default=None)
    prefer_date             = models.DateField( blank=True, null=True, default=None) 

    class Meta:
        db_table = 'register_user'    
