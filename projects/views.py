from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializer import ProjectSerializer,StatusSerializer,RoleSerializer,PermissionSerializer
from account.serializer import UserSerializer
from .models import Project,Status,Role,Permission
from account.models import User
from rest_framework import filters
from django.db.models import Q
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer


    def get_queryset(self):
        user = self.get_user()
        querySet = Project.objects.filter(Q(user=user)|Q(members__id=user))
        return querySet
    
    def perform_create(self, serializer):
        user = self.get_user()
        serializer.save(user=user)
    
    def perform_update(self, serializer):
        user = self.get_user()
        serializer.save(user=user)
    
    def get_user(self):
        print('user',self.request.user)
        user = self.request.user
        return user

    @action(methods=['get'] , detail=True)
    def members(self, request,pk=None):
        search = request.query_params.get('search','')
        project = self.get_object()
        members = project.members.filter(Q(email__icontains = search)| Q(first_name__icontains = search) | Q(last_name__icontains = search))
        serializer = UserSerializer(members, many=True)
        return Response(serializer.data)

    
        

class StatusViewSet(viewsets.ModelViewSet):
    serializer_class = StatusSerializer

    def get_queryset(self,*args, **kwargs):
        project = self.request.parser_context['kwargs'].get('project',None)
        querySet = Status.objects.filter(project__id = project)
        return querySet

        

class PermissionViewSet(viewsets.ModelViewSet):
    serializer_class = PermissionSerializer

    def get_queryset(self,*args, **kwargs):
        querySet = Permission.objects.all()
        return querySet



class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    search_fields = ['name','description']
    filter_backends = (filters.SearchFilter,)

    def perform_create(self, serializer):
        project = self.get_project()
        serializer.save(project=project)
    
    def perform_update(self, serializer):
        project = self.get_project()
        serializer.save(project=project)
    
    def get_project(self):
        user = self.request.user
        try:
            project = Project.objects.get(user =user,id = self.request.parser_context['kwargs'].get('project',None))
        except Project.DoesNotExist:
            raise ValidationError(
                {'detail': "Project does not exist"}
            )
        return project

    def get_queryset(self,*args, **kwargs):
        project = self.request.parser_context['kwargs'].get('project',None)
        querySet = Role.objects.filter(project__id = project)
        return querySet