from lib2to3.pgen2 import token
from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status

from account.serializer import WriteOnlyUserSerializer,ReadOnlyUserSerializer

from .models import User
from projects.models import Role
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from django.db.models import Q

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','signup']:
            return WriteOnlyUserSerializer
        return ReadOnlyUserSerializer

    def get_permissions(self):
        if self.action in ['create','signup','login']:
            self.permission_classes = []
        elif self.action in ['list']:
            self.permission_classes += [IsAdminUser]

        return super(UserViewSet, self).get_permissions()
        
    @action(detail=False, methods=['POST'])
    def signup(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({
            "user": self.get_serializer_class()(user,context=self.get_serializer_context()).data,
            "token": token.key
        },status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email, password=password)
        if len(user) > 0:
            token, created = Token.objects.get_or_create(user=user[0])
            return Response({
            'token': token.key,
            'user' : ReadOnlyUserSerializer(user[0]).data
            })
        return Response({
            'error':"email or password is incorrect"
        },status=status.HTTP_400_BAD_REQUEST)

   

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user' : ReadOnlyUserSerializer(user).data
    })