"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from rest_framework_simplejwt import views as jwt_views
from Physiotherapist import views
from django.conf.urls import  handler500,handler404
from Auth import views as au
from django.conf.urls import url

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from clinic import views as cli
from episode import views as ep
from exercise import views as ex
from patient import views as vi
from Mobile import views as mo


schema_view = get_schema_view(
   openapi.Info(
      title="Physio API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="mishra.satwik9532@gmail.com"),
      license=openapi.License(name="Test License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)









urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/register_physio/', views.Reg_physio),
    path('api/get_physio/', views.get_physio),
     path('api/get_single_physio/', views.get_single_physio),
   
   # path('api/login/',jwt_views.TokenObtainPairView.as_view(),name ='token_obtain_pair'),
    path('api/login/',views.login),
    path('api/logout/',views.logout),
    path('api/update_profile/',views.update_profile),
    path('api/profile',views.profile),
    path('api/validate_email/',views.validate_email),
    path('api/validate_mobile/',views.validate_mobile),
    path('api/email-varification/',views.otp_varification),
    path('api/reset-password/',views.reset_password),
    path('api/physio-filter/',views.physio_search),
       path('api/add-clinic/',cli.add_clinic),
    path('api/get-clinic/',cli.get_clinic),
    path('api/send/',views.mail),
    path('api/password_reset/', au.password_change_request),
    path('api/password_reset_confirm/', au.reset_password_confirm),
    path('api/password_reset_by_admin/', au.admin_password_reset),
    path('api/register/', au.add_register_user),
     path('api/calendar/', au.get_calendar),




    path('api/add-patient/', vi.patient_reg),
    path('api/update-patient/', vi.update_patient),
    path('api/get-patient/', vi.get_patient),
    path('api/search-patient/', vi.search),
    path('api/validate_mobile/', vi.validate_mobile),
    path('api/patient-profile/', vi.patient_profile),
    path('api/patient-profile/<int:id>', vi.patient_profile),





    path('api/mobile/get-care-plan/', mo.get_care_plan),
     path('api/get-exercise/', ex.get_exercise),
    path('api/exercise_detail/', ex.exercise_detail),
    path('api/exercise-filter/', ex.search_exercise),
    path('api/exercise-joints/', ex.exercise_base_on_joints),
    path('api/add-care-plan/', ex.add_care_plan),
    path('api/get-care-plan/', ex.get_care_plan),
    path('api/get-care-plan_mobile/', ex.get_care_plan_mobile),
    path('api/get-all-care-plan/', ex.get_all_care_plan),
    path('api/update_care_plan/', ex.update_care_plan_status),
     path('api/add_assessment/', ep.add_assessment_1),
     path('api/add_episode/', ep.add_episode_1),
     path('api/get_episode/', ep.get_episode),
     path('api/get_episode/<int:id>', ep.get_episode),
     path('api/get_active_episode/', ep.get_active_episode),
     path('api/add_visit/', ep.add_visit),
     path('api/get_visit/', ep.get_visit),
     path('api/delete_visit/', ep.delete_visit),
     path('api/get_visit/<int:id>', ep.get_visit),
     path('api/test_get_visit/<int:pk>', ep.test_get_visit),
     path('api/get_visit_physio/', ep.get_visit_by_physio),
     path('api/test_assessment/', ep.insert_asse_test),
    path('api/get_assessment/', ep.get_assessment),
    path('api/add_questions/', ep.questions),
    path('api/get_questions/', ep.get_question),
    path('api/update_episode/', ep.update_episode),
    path('api/update_visit/', ep.update_visit),
    path('api/patient_visit/', ep.patient_visit),
    path('api/add_pres/', ep.add_pres),
    path('api/get_pres/', ep.get_pres),
    path('api/dashboard/', ep.dashboard),
    path('api/patient-dashboard/', ep.patient_dashboard),
    path('api/patient-progress/', ep.progress_1),
    path('api/add-notes/', ep.add_notes),
    path('api/get-notes/', ep.get_notes),
    path('api/get_patient_assessment/', ep.patient_assessment),
    path('api/get/test_assessment/', ep.get_asse_test),
    path('api/basic_detail/', ep.basic_detail),
    path('api/uploadedfiles/<str:slug>/', ep.file_download),



	




  

    path('swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


]
handler500 = 'Physiotherapist.views.error_500'
handler404 = 'Physiotherapist.views.error_404'
 
