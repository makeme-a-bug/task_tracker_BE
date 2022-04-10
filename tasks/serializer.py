from sys import meta_path
from urllib import request
from rest_framework import serializers
from .models import Task , Issue , TaskComment , IssueComment
from projects.serializer import StatusSerializer



class WriteOnlyTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ['user','project']

# issue serialziers
class WriteOnlyIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"
        read_only_fields = ['user','task']



class ReadOnlyIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"
        read_only_fields = ['user','task']
        depth=1

#--------------------------------------------
# task comment serializers

class ReadOnlyTaskCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = "__all__"    
        read_only_fields = ['user','task']
        depth=1

class WriteOnlyTaskCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = "__all__"    
        read_only_fields = ['user','task']
        depth=1

#-----------------------------------------------

# issue comment serializers

class WriteOnlyIssueCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueComment
        fields = "__all__"
        read_only_fields = ['user','issue']


class ReadOnlyIssueCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueComment
        fields = "__all__"
        read_only_fields = ['user','issue']
        depth = 1
class ReadOnlyTaskSerializer(serializers.ModelSerializer):
    status = StatusSerializer(read_only = True)
    taskcomment_set = ReadOnlyTaskCommentSerializer(read_only=True , many=True)
    issue_set = ReadOnlyIssueSerializer(read_only=True , many=True)
    
    class Meta:
        model = Task
        fields = "__all__"
        depth = 1