from rest_framework.serializers import ModelSerializer
from .models import UserModel


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['name', 'email', 'phone', 'role', 'create_at', 'update_at']
