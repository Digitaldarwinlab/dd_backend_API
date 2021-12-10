from django.contrib import admin
from Physiotherapist.models import pp_physiotherapist_master,pp_otp,old_password
# Register your models here.
admin.site.register(pp_physiotherapist_master)
admin.site.register(pp_otp)
admin.site.register(old_password)

