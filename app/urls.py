
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


    path('api/createvotingcode/',apiview.CreateVotingView.as_view(),name='create_v'),
    path('api/checkcode/',apiview.CheckVotingCode.as_view(),name='check_code'),
    path('api/votingm/',apiview.VotingMView.as_view(),name='voting'),
    path('api/registerdevice/',apiview.RegisterNewDevice.as_view(),name='register_device'),


    path('api/selectionqueen/',apiview.SelectionQueen.as_view(),name='selectionqueen'),
    path('api/selectionking/',apiview.SelectionKing.as_view(),name='selectionking'),

    # retun Image
    path('api/selectionkingimage/',apiview.KingImage.as_view(),name='selectionkingimage'),
    path('api/selectionqueenimage/',apiview.QueenImage.as_view(),name='selectionqueenimage'),


    #return Result 
    path('api/kingresult/',apiview.KingResult.as_view(),name='kingresult'),
    path('api/queenresult/',apiview.QueenResult.as_view(),name='queenresult'),

    path('api/voteking/',apiview.VoteKing.as_view(),name='voteking'),
    path('api/votequeen/',apiview.VoteQueen.as_view(),name='votequeen'),    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
