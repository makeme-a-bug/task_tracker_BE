from rest_framework import serializers

from .models import User
from projects.serializer import RoleSerializerDepth 


class ReadOnlyUserSerializer(serializers.ModelSerializer):
    role_set = serializers.SerializerMethodField()
    
    def get_role_set(self,obj):
        if self.context.get('project',None):
            data = RoleSerializerDepth(obj.role_set.filter(project_id = self.context.get('project')),many=True).data
            return data
        return None
    class Meta:
        model = User
        exclude=["password"]

class WriteOnlyUserSerializer(serializers.ModelSerializer):
    
    def get_role_set(self,obj):
        if self.context.get('project',None):
            data = RoleSerializerDepth(obj.role_set.filter(project_id = self.context.get('project')),many=True).data
            return data
        return None
    class Meta:
        model = User
        fields='__all__'

    



