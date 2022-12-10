from django.urls import path, include

# from app.models import SalesTwoDigits
from . import views
from . import apiview
from django.conf.urls.static import static
from django.conf import settings


from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
   


    path('auth/login/', obtain_auth_token, name='auth_user_login'),
    path('auth/register/', apiview.CreateUserApiView.as_view(),
         name='auth_user_create'),

    path('api/checkcode/',apiview.CheckVotingCode.as_view(),name='check_code'),
    path('api/votingm/',apiview.VotingMView.as_view(),name='voting'),
    path('api/registerdevice/',apiview.RegisterNewDevice.as_view(),name='register_device')

    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
