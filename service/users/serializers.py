from profiles.models import User
from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = ('is_active', 'is_staff', 'password', 'last_login',  'groups', 'user_permissions', )