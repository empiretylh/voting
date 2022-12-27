from rest_framework import serializers
from django.contrib.auth import get_user_model
from . import models

from django.utils import timezone

class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = ['name', 'username', 'email', 'phoneno', 'password']
        write_only_fields = ('password')

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Device 
        fields = ['id','deviceid','name','votingm']


class SelectionImageKingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SelectionImageKing
        fields = ['id','image','sk']



class SelectionImageQueenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SelectionImageQueen
        fields = ['id','image','sk']


class SelectionKingSerializer(serializers.ModelSerializer):
    images = SelectionImageKingSerializer(many=True,read_only=True)

    class Meta:
        model = models.SelectionKing
        fields = ['id','name','year','fblink','iglink','user','vm','is_male','profileimage','images']


class SelectionQueenSerializer(serializers.ModelSerializer):
    images = SelectionImageQueenSerializer(many=True,read_only=True)
   
    class Meta:
        model = models.SelectionQueen
        fields = ['id','name','year','fblink','iglink','user','vm','is_male','profileimage','images']



class FinishKingGroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.FinishKingGroup
        fields= ['id','device','selection']


class FinishQueenGroupSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = models.FinishQueenGroup
        fields= ['id','device','selection']


class VotingMSerializer(serializers.ModelSerializer):
    # devices = DeviceSerializer(many=True,read_only=True)
    sel_king = SelectionKingSerializer(many=True,read_only=True)
    sel_queen = SelectionQueenSerializer(many=True,read_only=True)
    class Meta: 
        model = models.VotingM
        fields = ['id','votingcode','title','is_start','is_end','end_time','user','sel_king','sel_queen']


