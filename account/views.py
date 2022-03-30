from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import viewsets

from account.serializer import UserSerializer,TeamSerializer

from .models import User,Team




class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = []
        elif self.action in ['list']:
            permission_classes = [IsAdminUser,IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    # def get_authenticators(self):
    #     if self.action in ['create']:
    #         authentication_classes = []
    #     else:
    #         authentication_classes = [TokenAuthentication]
    #     return [authenticator() for authenticator in authentication_classes]

class TeamViewSet(viewsets.ModelViewSet):

    serializer_class = TeamSerializer
    queryset = Team.objects.all()    