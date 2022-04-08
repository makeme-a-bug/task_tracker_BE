from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from account.serializer import UserSerializer

from .models import User
from projects.models import Role
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action in ['create',"removeRole","addRole"]:
            permission_classes = []
        elif self.action in ['list']:
            permission_classes = [IsAdminUser,IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True,methods=['PUT'])
    def addRole(self,request,pk=None):
        role = self.request.data.get('role',None)
        if role:
            user = User.objects.get(id=pk)
            try:
                role = Role.objects.get(id=role,project__user__id = pk)
            except Role.DoesNotExist:
                raise ValidationError('Role does not exist')
            user.role_set.add(role)
            serializer = self.serializer_class(user)
            return Response(serializer.data)
        else:
            return Response({'error':'role is required'})

    @action(detail=True,methods=['PUT'])
    def removeRole(self,request,pk=None):
        role = self.request.data.get('role',None)
        if role:
            user = User.objects.get(id=pk)
            try:
                role = Role.objects.get(id=role,project__user__id = pk)
            except Role.DoesNotExist:
                raise ValidationError('Role does not exist')
            user.role_set.remove(role)
            serializer = self.serializer_class(user)
            return Response(serializer.data)
        else:
            return Response({'error':'role is required'})

    # def get_authenticators(self):
    #     if self.action in ['create']:
    #         authentication_classes = []
    #     else:
    #         authentication_classes = [TokenAuthentication]
    #     return [authenticator() for authenticator in authentication_classes]


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user' : UserSerializer(user).data
    })