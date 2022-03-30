from django.shortcuts import render

from rest_framework import viewsets

from .serializer import ProjectSerializer,StatusSerializer
from .models import Project,Status


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        querySet = Project.objects.all()
        return querySet
    
    # def perform_create(self, serializer):
    #     user,task = self.get_user_task()
    #     serializer.save(user=user,task = task)
    
    # def perform_update(self, serializer):
    #     user,task = self.get_user_task()
    #     serializer.save(user=user,task = task)
    
    # def get_user_task(self):
    #     user = User.objects.get(email = "admin@gmail.com")
    #     task = Task.objects.get(id = self.request.parser_context['kwargs'].get('task',None))
    #     return user , task

class StatusViewSet(viewsets.ModelViewSet):
    serializer_class = StatusSerializer

    def get_queryset(self,*args, **kwargs):
        project = self.request.parser_context['kwargs'].get('project',None)
        querySet = Status.objects.filter(project__id = project)
        return querySet