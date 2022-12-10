import operator
import functools
import collections
from collections import OrderedDict
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from django.utils import timezone


from . import models, serializers

import json


def CHECK_IN_PLAN_AND_RESPONSE(user,data,**args):
    if  user.is_plan:
        return Response('End Plan or No Purchase Plan')
    else:
        return Response(data=data,**args)

    print('User is in Plan')

class CreateUserApiView(CreateAPIView):

    permission_classes = [AllowAny]
    serializer_class = serializers.CreateUserSerializer

    def post(self, request):
        print('posteed')
        print(request.data)
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        self.perform_create(serializers)
        headers = self.get_success_headers(serializers.data)

        # Create a token than will be used for future auth
        token = Token.objects.create(user=serializers.instance)
        token_data = {'token': token.key}

        return Response(
            {**serializers.data, **token_data},
            status=status.HTTP_201_CREATED,
            headers=headers)

class CreateVotingView(APIView):


     def post(self,request):
        title = request.data['title']
        user =  get_user_model().objects.get(username=request.user)
        end_time = request.data['endtime']
        models.VotingM.objects.create(user=user,title=title,end_time=end_time)

        return Response(status=status.HTTP_201_CREATED)

     def get(self,request):
        user = get_user_model().objects.get(username=request.user)
        voting = models.VotingM.objects.get(user=user,is_end=False);
        vserializer = serializers.VotingMSerializer(voting,many=True)
        return Response(vserializer.data)






class CheckVotingCode(APIView):
    permissions_classes = [AllowAny]

    def get(self,request):
        votingcode = request.GET.get('votingcode')

        try:
            v_data = models.VotingM.objects.get(id=votingcode,is_end=False)
            return Response(1)
        except ObjectDoesNotExist:
            print('ObjectDoesNotExist')
            return Response('This Voting Code is Invalid')



class VotingMView(APIView):
    permissions_classes = [AllowAny]

    def get(self,request):
        votingcode = request.GET.get('votingcode')

        try:
            v_data = models.VotingM.objects.get(id=votingcode,is_end=False)
            ser = serializers.VotingMSerializer(v_data)
        
            return Response(ser.data);

        except ObjectDoesNotExist:
            return Response('This Voting Code is Invalid')
        


class SelectionKing(APIView):
    permissions_classes=[AllowAny]

    def post(self,request):
        name = request.data['name']
        year = request.data['year']
        iglink = request.data['iglink']
        fblink = request.data['fblink']
        user =  get_user_model().objects.get(username=request.user)

        models.SelectionKing.objects.create(name=name,year=year,iglink=iglink,fblink=fblink)
            
        return Response(status=status.HTTP_201_CREATED)

    #Client Can Request This View

    def get(self,request):
        votingcode = request.data['votingcode']
        voting = models.VotingM.objects.get(id=votingcode)
        

class RegisterNewDevice(APIView):
    permission_classes= [AllowAny]

    def post(self,request):
        dvid = request.data['deviceid']
        name = request.data['name']
        votingcode = request.data['votingcode']
        voting = models.VotingM.objects.get(id=votingcode,is_end=False)
        try:
            is_has = models.Device.objects.get(votingm=voting,deviceid=dvid)
            is_has.name = name;
            is_has.save();
            print('Devices Is Already Registred');
            return Response(status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            mdels.Device.objects.create(votingm=voting,name=name,deviceid=dvid)
            print('New Devices Created');
            return Response(status=status.HTTP_201_CREATED)


