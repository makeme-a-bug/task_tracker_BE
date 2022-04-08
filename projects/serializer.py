from sys import meta_path
from rest_framework import serializers

from .models import Project,Status,Role,Permission


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"
        read_only_fields=['project']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields=['user']
        depth=1

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"
        

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
        read_only_fields=['project','deletable']
        
class RoleSerializerDepth(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
        read_only_fields=['project','deletable']
        depth = 1


