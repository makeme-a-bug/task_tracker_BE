from rest_framework import serializers

from .models import User
from projects.serializer import RoleSerializerDepth 


class UserSerializer(serializers.ModelSerializer):
    role_set = RoleSerializerDepth(many=True)
    class Meta:
        model = User
        exclude=["password"]



