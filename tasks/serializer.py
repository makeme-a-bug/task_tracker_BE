from sys import meta_path
from urllib import request
from rest_framework import serializers
from .models import Task , Issue , TaskComment , IssueComment
from projects.serializer import StatusSerializer

class ReadonlyTaskSerializer(serializers.ModelSerializer):
    status = StatusSerializer(read_only = True)
    class Meta:
        model = Task
        fields = "__all__"
        depth = 1

class WriteOnlyTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ['user','project']

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"
        read_only_fields = ['user','task']


class TaskCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = "__all__"    
        read_only_fields = ['user','task']


class IssueCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueComment
        fields = "__all__"
        read_only_fields = ['user','issue']