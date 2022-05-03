# Django
from rest_framework.test import APITestCase

# models
from profiles.models import Profile
from users.models import User

class ProfileTestCase(APITestCase):

    def setUp(self):

        self.user_email = 'luis@code.bo'
        self.user_password = 'luis'

        self.user = User.objects.create_user(email=self.user_email, password=self.user_password)
        self.user.save()
        self.profile = Profile.objects.create(user=self.user, first_name='Luis', last_name='Andrade', description='Senior Python', email='luis@gmail.com', phone='+591 65756565', git='https://github.com/luis')

    def test_create_profile_model(self):

        first_profile = Profile.objects.get( email='luis@gmail.com')
        first_user = User.objects.get( email='luis@code.bo')
        self.assertIsNotNone(first_profile)
        self.assertEqual(first_profile.user, first_user)
        self.assertEqual(first_profile.first_name, 'Luis')
        self.assertEqual(first_profile.last_name, 'Andrade')
        self.assertEqual(first_profile.description, 'Senior Python')
        self.assertEqual(first_profile.email, 'luis@gmail.com')
        self.assertEqual(first_profile.phone, '+591 65756565')
        self.assertEqual(first_profile.git, 'https://github.com/luis')
