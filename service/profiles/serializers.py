from profiles.models import Profile
from rest_framework.serializers import ModelSerializer
from users.serializers import UserSerializer
class ProfileSerializer(ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Profile
        exclude = ('created_date', 'modified_date', 'delete_date',)