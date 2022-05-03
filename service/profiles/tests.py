# Django
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
import ast

# models
from profiles.models import Profile
from users.models import User

class ProfileTestCase(APITestCase):

    def setUp(self):

        self.url_jwt = reverse("token_obtain_pair")
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

    def test_get_jwt(self):
        credentials = {
            'email': self.user_email,
            'password': self.user_password,
        }
        response = self.client.post(self.url_jwt, credentials, format="json")
        content = ast.literal_eval(response.content.decode("UTF-8"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(content['access'])
        self.assertIsNotNone(content['refresh'])

    def test_url_profile_markdown_success(self):
        credentials = {
            'email': self.user_email,
            'password': self.user_password,
        }
        response_jwt = self.client.post(self.url_jwt, credentials, format="json")
        content = ast.literal_eval(response_jwt.content.decode("UTF-8"))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + content["access"])
        id = str(self.profile.id)
        response_profile_markdown = self.client.get(reverse("profile:profile_md", args=[id]))
        response_profile_markdown_content = str(response_profile_markdown.content.decode("UTF-8"))

        self.assertEqual(response_jwt.status_code, status.HTTP_200_OK)
        self.assertEqual(response_profile_markdown.status_code, status.HTTP_200_OK)
        # self.assertEqual(response_profile_markdown.content_type, 'text/plain')
        self.assertTrue(self.profile.email in response_profile_markdown_content )
        self.assertTrue(self.profile.first_name in response_profile_markdown_content)
        self.assertTrue(self.profile.last_name in response_profile_markdown_content)

    def test_url_profile_markdown_401_unauthorized_without_jwt(self):
        id = str(self.profile.id)
        response_profile_markdown = self.client.get(reverse("profile:profile_md", args=[id]))
        self.assertEqual(response_profile_markdown.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_url_profile_markdown_404_not_found(self):
        credentials = {
            'email': self.user_email,
            'password': self.user_password,
        }
        response_jwt = self.client.post(self.url_jwt, credentials, format="json")
        content = ast.literal_eval(response_jwt.content.decode("UTF-8"))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + content["access"])
        id = '12312312h123h123211vf2_123'
        response_profile_markdown = self.client.get(reverse("profile:profile_md", args=[id]))
        self.assertEqual(response_profile_markdown.status_code, status.HTTP_404_NOT_FOUND)
