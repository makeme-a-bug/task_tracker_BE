from django.shortcuts import render

from rest_framework import viewsets

from account.models import User

from projects.models import Project

from .serializer import ReadonlyTaskSerializer , WriteOnlyTaskSerializer , IssueSerializer , TaskCommentSerializer , IssueCommentSerializer
from .models import Task, Issue , TaskComment , IssueComment

class TasksViewSet(viewsets.ModelViewSet):

    def get_queryset(self,*args, **kwargs):
        project = self.request.parser_context['kwargs'].get('project',None)
        queryset =  Task.objects.filter(project__id = project)
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            serializer_class = WriteOnlyTaskSerializer
        else:
            serializer_class = ReadonlyTaskSerializer
        return serializer_class

    def perform_create(self, serializer):
        user,project = self.get_user_project()
        serializer.save(user=user,project = project)
    
    def perform_update(self, serializer):
        user,project = self.get_user_project()
        serializer.save(user=user,project = project)
    
    def get_user_project(self):
        user = User.objects.get(email = "admin@gmail.com")
        project = Project.objects.get(id = self.request.parser_context['kwargs'].get('project',None))
        return user , project


    

class IssueViewSet(viewsets.ModelViewSet):

    serializer_class = IssueSerializer

    def get_queryset(self,*args, **kwargs):
        task = self.request.parser_context['kwargs'].get('task',None)
        queryset =  Issue.objects.filter(task__id = task)
        return queryset

    def perform_create(self, serializer):
        user,task = self.get_user_task()
        serializer.save(user=user,task = task)
    
    def perform_update(self, serializer):
        user,task = self.get_user_task()
        serializer.save(user=user,task = task)
    
    def get_user_task(self):
        user = User.objects.get(email = "admin@gmail.com")
        task = Task.objects.get(id = self.request.parser_context['kwargs'].get('task',None))
        return user , task


class TaskCommentViewSet(viewsets.ModelViewSet):
    serializer_class = TaskCommentSerializer


    def get_queryset(self,*args, **kwargs):
        task = self.request.parser_context['kwargs'].get('task',None)
        queryset =  TaskComment.objects.filter(task__id = task)
        return queryset
    
    def perform_create(self, serializer):
        user,task = self.get_user_task()
        serializer.save(user=user,task = task)
    
    def perform_update(self, serializer):
        user,task = self.get_user_task()
        serializer.save(user=user,task = task)
    
    def get_user_task(self):
        user = User.objects.get(email = "admin@gmail.com")
        task = Task.objects.get(id = self.request.parser_context['kwargs'].get('task',None))
        return user , task

class IssueCommentViewSet(viewsets.ModelViewSet):
    serializer_class = IssueCommentSerializer

    def get_queryset(self,*args, **kwargs):
        issue = self.request.parser_context['kwargs'].get('issue',None)
        queryset =  IssueComment.objects.filter(issue__id = issue)
        return queryset

    def perform_create(self, serializer):
        user,issue = self.get_user_issue()
        serializer.save(user=user,issue = issue)
    
    def perform_update(self, serializer):
        user,issue = self.get_user_issue()
        serializer.save(user=user,issue = issue)
    
    def get_user_issue(self):
        user = User.objects.get(email = "admin@gmail.com")
        issue = Issue.objects.get(id = self.request.parser_context['kwargs'].get('issue',None))
        return user , issue

    
# Create your views here.
