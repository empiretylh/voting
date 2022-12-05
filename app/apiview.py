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

