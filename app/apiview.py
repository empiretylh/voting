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

import random

# Generate a random number between 100 and 999

class CreateVotingView(APIView):


     def post(self,request):
        title = request.data['title']
        user =  get_user_model().objects.get(username=request.user)

        end_time = request.data['endtime']
        print(end_time)
        
        v  = models.VotingM.objects.create(user=user,title=title,end_time=end_time)
        v.votingcode = 1000 + v.id
        v.save()
        return Response(v.votingcode)

     def put(self,request):
        user = get_user_model().objects.get(username=request.user)
        votingcode =request.data['votingcode']
        end_time = request.data['endtime']


        voting = models.VotingM.objects.get(user=user,votingcode=votingcode)
        voting.end_time = end_time

        voting.save()
        vserializer = serializers.VotingMSerializer(voting)
        return Response(vserializer.data)


     def get(self,request):
        user = get_user_model().objects.get(username=request.user)
        voting = models.VotingM.objects.filter(user=user);
        vserializer = serializers.VotingMSerializer(voting,many=True)
        return Response(vserializer.data)

     def delete(self,request):
        id = request.GET.get('id')  
        user = get_user_model().objects.get(username=request.user)
       
        v = models.VotingM.objects.get(user=user,id=id)
        v.delete() 
        return Response(1)

#return Individal Voting ID and it datas

class VoteKing(APIView):

    permission_classes = [AllowAny]

    def post(self,request):
        votingcode = request.data['votingcode']
        kingid = request.data['kingid']
        dvid = request.data['deviceid']
        v_data = models.VotingM.objects.get(votingcode=votingcode,is_end=False)
           
        sel_king = models.SelectionKing.objects.get(vm=v_data,id=kingid)
        device = models.Device.objects.get(votingm=v_data,deviceid=dvid)

        try:
            models.FinishKingGroup.objects.get(device=device,vm=v_data)
            print('Object Already Exists')
            return Response(0)
        except ObjectDoesNotExist:
            print('Successfully Voted')
            group = models.FinishKingGroup.objects.create(device=device,selection=sel_king,vm=v_data)

            return Response(status=status.HTTP_201_CREATED)

    #Return Device Voted King
    def get(self,request):
        dvid = request.GET.get('deviceid')
        votingcode = request.GET.get('votingcode')
        v_data = models.VotingM.objects.get(votingcode=votingcode)
        try:
            voted = models.FinishKingGroup.objects.get(device__deviceid=dvid,vm=v_data)
            ser = serializers.FinishKingGroupSerializer(voted)
            return Response(ser.data)
        except ObjectDoesNotExist:
            print('King Voted Objects Not Exists')
            return Response(0)

    def delete(self,request):
        dvid = request.GET.get('deviceid')
        votingcode = request.GET.get('votingcode')
        voted = models.FinishKingGroup.objects.get(device__deviceid=dvid,vm__votingcode=votingcode)
        voted.delete()
        print('Successfully Deleted Voting')
        return Response(1)


class VoteQueen(APIView):

    def post(self,request):
        votingcode = request.data['votingcode']
        queenid = request.data['queenid']
        dvid = request.data['deviceid']
        v_data = models.VotingM.objects.get(votingcode=votingcode,is_end=False)
           
        sel_queen = models.SelectionQueen.objects.get(vm=v_data,id=queenid)
        device = models.Device.objects.get(votingm=v_data,deviceid=dvid)
        try:
            models.FinishQueenGroup.objects.get(device=device,vm=v_data)
            print('Object Already Exists')
            return Response(0)
        except ObjectDoesNotExist:
            group = models.FinishQueenGroup.objects.create(device=device,selection=sel_queen,vm=v_data)
            print('Successfully Voted')
            return Response(status=status.HTTP_201_CREATED)

    #Return Device Voted Queen
    def get(self,request):
        dvid = request.GET.get('deviceid')
        votingcode = request.GET.get('votingcode')
        v_data = models.VotingM.objects.get(votingcode=votingcode)

        try:
            voted = models.FinishQueenGroup.objects.get(device__deviceid=dvid,vm=v_data)
            ser = serializers.FinishQueenGroupSerializer(voted)
            return Response(ser.data)
        except ObjectDoesNotExist:
            print('Queen Voted Objects Not Exists')
            return Response(0)

    def delete(self,request):
        dvid = request.GET.get('deviceid')
        votingcode = request.GET.get('votingcode')
        voted = models.FinishQueenGroup.objects.get(device__deviceid=dvid,vm__votingcode=votingcode)
        voted.delete()
        print('Successfully Deleted Voting')
        return Response(1)

        

class CheckVotingCode(APIView):
    permissions_classes = [AllowAny]

    def get(self,request):
        votingcode = request.GET.get('votingcode')
           

        try:
            v_data = models.VotingM.objects.get(votingcode=votingcode,is_end=False)
            return Response(1)
        except ObjectDoesNotExist:
            print('ObjectDoesNotExist')
            return Response('This Voting Code is Invalid')



#return Individal Voting ID and it datas
class VotingMView(APIView):
    permissions_classes = [AllowAny]

    def get(self,request):
        votingcode = request.GET.get('votingcode')

        try:
            v_data = models.VotingM.objects.get(votingcode=votingcode,is_end=False)
            ser = serializers.VotingMSerializer(v_data)
        
            return Response(ser.data);

        except ObjectDoesNotExist:
            return Response('This Voting Code is Invalid')
        


class SelectionKing(APIView):
    permissions_classes=[AllowAny]

    def post(self,request,format=None):
        name = request.data['name']
        year = request.data['year']
        iglink = request.data['iglink']
        fblink = request.data['fblink']
        votingcode = request.data['votingcode']
        pfimage = request.data['profileimage']
    
        user =  get_user_model().objects.get(username=request.user)
        voting = models.VotingM.objects.get(votingcode=votingcode,user=user)
        md = models.SelectionKing.objects.create(name=name,year=year,iglink=iglink,fblink=fblink,vm=voting,user=user)
            
        print(pfimage)
        if not pfimage == 'null':
            md.profileimage = pfimage
            md.save()

        return Response(status=status.HTTP_201_CREATED)

    #Client Can Request This View

    def get(self,request):
        votingcode = request.GET.get('votingcode')
        voting = models.VotingM.objects.get(votingcode=votingcode)
        k_s = models.SelectionKing.objects.filter(vm=voting)

        ser = serializers.SelectionKingSerializer(k_s,many=True)

        return Response(ser.data)

    def delete(self,request):
        kingid = request.GET.get('id')
        votingcode = request.GET.get('votingcode')
        user = get_user_model().objects.get(username=request.user)
        voting = models.VotingM.objects.get(votingcode=votingcode,user=user)
        king = models.SelectionKing.objects.get(vm=voting,user=user,id=kingid)
        king.delete()

        return Response(status=status.HTTP_201_CREATED)



class SelectionQueen(APIView):
    permissions_classes=[AllowAny]

    def post(self,request):
        name = request.data['name']
        year = request.data['year']
        iglink = request.data['iglink']
        fblink = request.data['fblink']
        votingcode = request.data['votingcode']
        pfimage = request.data['profileimage']
        user =  get_user_model().objects.get(username=request.user)
        voting = models.VotingM.objects.get(votingcode=votingcode,user=user)
        models.SelectionQueen.objects.create(name=name,year=year,iglink=iglink,fblink=fblink,profileimage=pfimage,vm=voting,user=user)
            
        return Response(status=status.HTTP_201_CREATED)

    #Client Can Request This View

    def get(self,request):
        votingcode = request.GET.get('votingcode')
        voting = models.VotingM.objects.get(votingcode=votingcode)
        k_s = models.SelectionQueen.objects.filter(vm=voting)

        ser = serializers.SelectionQueenSerializer(k_s,many=True)
        
        return Response(ser.data)

    def delete(self,request):
        queenid = request.GET.get('id')
        votingcode = request.GET.get('votingcode')
        user = get_user_model().objects.get(username=request.user)
        voting = models.VotingM.objects.get(votingcode=votingcode,user=user)
        queen = models.SelectionQueen.objects.get(vm=voting,user=user,id=queenid)
        queen.delete()

        return Response(status=status.HTTP_201_CREATED)

class KingImage(APIView):
    permissions_classes=[AllowAny]

    def post(self,request):
        kingid = request.data['person_id']
        image = request.data['image']
        user = get_user_model().objects.get(username=request.user)
        king = models.SelectionKing.objects.get(user=user,id=kingid)
        models.SelectionImageKing.objects.create(sk=king,image=image,user=user)

        return Response(status=status.HTTP_201_CREATED)

    def get(self,request):
        kingid = request.GET.get('kingid')
        user = get_user_model().objects.get(username=request.user)
        king = models.SelectionKing.objects.get(user=user,id=kingid)
        i_k  = models.SelectionImageKing.objects.filter(sk=king,user=user)
        ser = serializers.SelectionImageKingSerializer(i_k,many=True)
        return Response(ser.data)




class QueenImage(APIView):
    permissions_classes=[AllowAny]

    def post(self,request):
        kingid = request.data['person_id']
        image = request.data['image']
        user = get_user_model().objects.get(username=request.user)
        king = models.SelectionQueen.objects.get(user=user,id=kingid)
        models.SelectionImageQueen.objects.create(sk=king,image=image,user=user)

        return Response(status=status.HTTP_201_CREATED)

    def get(self,request):
        kingid = request.GET.get('queenid')
        user = get_user_model().objects.get(username=request.user)
        king = models.SelectionQueen.objects.get(user=user,id=kingid)
        i_k  = models.SelectionImageQueen.objects.filter(sk=king,user=user)
        ser = serializers.SelectionImageQueenSerializer(i_k,many=True)
        return Response(ser.data)


class KingResult(APIView):
    # permissions_classes=[AllowAny]

    def get(self,request):
        user = get_user_model().objects.get(username=request.user)
        votingcode = request.GET.get('votingcode')
        v_data = models.VotingM.objects.get(votingcode=votingcode,user=user)

        try:
            voted = models.FinishKingGroup.objects.filter(vm=v_data)
            ser = serializers.FinishKingGroupSerializer(voted,many=True)
            return Response(ser.data)
        except ObjectDoesNotExist:
          
            return Response(0)


class QueenResult(APIView):
    # permissions_classes=[AllowAny]

    def get(self,request):
        votingcode = request.GET.get('votingcode')
        user = get_user_model().objects.get(username=request.user)
        v_data = models.VotingM.objects.get(votingcode=votingcode,user=user)

        try:
            voted = models.FinishQueenGroup.objects.filter(vm=v_data,)
            ser = serializers.FinishQueenGroupSerializer(voted,many=True)
            return Response(ser.data)
        except ObjectDoesNotExist:
            # print('Queen Voted Objects Not Exists')
            return Response(0)



class RegisterNewDevice(APIView):
    permission_classes= [AllowAny]

    def post(self,request):
        dvid = request.data['deviceid']
        name = request.data['name']
        votingcode = request.data['votingcode']
        voting = models.VotingM.objects.get(votingcode=votingcode,is_end=False)
        try:
            is_has = models.Device.objects.get(votingm=voting,deviceid=dvid)
            is_has.name = name;
            is_has.save();
            print('Devices Is Already Registred');
            return Response(status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            models.Device.objects.create(votingm=voting,name=name,deviceid=dvid)
            print('New Devices Created');
            return Response(status=status.HTTP_201_CREATED)


