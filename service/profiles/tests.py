# Django
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
import ast

# models
from profiles.models import Profile, CategorySkill, Skill
from users.models import User

class ProfileTestCase(APITestCase):

    def setUp(self):

        self.url_jwt = reverse("token_obtain_pair")
        self.user_email = 'luis@code.bo'
        self.user_password = 'luis'

        self.user = User.objects.create_user(email=self.user_email, password=self.user_password)
        self.user.save()
        self.profile = Profile.objects.create(user=self.user, first_name='Luis', last_name='Andrade', description='Senior Python', email='luis@gmail.com', phone='+591 65756565', git='https://github.com/luis')

        self.languages = CategorySkill.objects.create(name_category='Idiomas', profile=self.profile)
        self.languages_programming = CategorySkill.objects.create(name_category='Lenguajes de programacion', profile=self.profile)
        self.as_a_person = CategorySkill.objects.create(name_category='Como Persona', profile=self.profile)

        self.skill_languages_1 = Skill.objects.create(name='Español', level=4)
        self.skill_languages_1.category_skill.set([self.languages])

        self.skill_languages_2 = Skill.objects.create(name='English', level=1)
        self.skill_languages_2.category_skill.set([self.languages])

        self.skill_languages_programming_1 = Skill.objects.create(name='Python', level=2)
        self.skill_languages_programming_1.category_skill.set([self.languages_programming])

        self.skill_languages_programming_2 = Skill.objects.create(name='Javascript', level=2)
        self.skill_languages_programming_2.category_skill.set([self.languages_programming])

        self.skill_as_a_person_1 = Skill.objects.create(name='Liderazgo')
        self.skill_as_a_person_1.category_skill.set([self.as_a_person])

        self.skill_as_a_person_2 = Skill.objects.create(name='Honestidad')
        self.skill_as_a_person_2.category_skill.set([self.as_a_person])

        self.skill_as_a_person_3 = Skill.objects.create(name='Trabajo en Equipo')
        self.skill_as_a_person_3.category_skill.set([self.as_a_person])
        self.profile.save()


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

    def test_create_skill_model(self):
        first_profile = Profile.objects.get(email='luis@gmail.com')
        category_skill_query = CategorySkill.objects.filter(profile=first_profile)
        skill_query = {}
        for cat in category_skill_query:
            skill_query[cat] = Skill.objects.filter(category_skill=cat)

        self.assertIsNotNone(category_skill_query)
        self.assertIsNotNone(skill_query)
        self.assertTrue(self.languages in category_skill_query)
        self.assertTrue(self.languages_programming in category_skill_query)
        self.assertTrue(self.as_a_person in category_skill_query)
        self.assertTrue(self.skill_languages_1 in skill_query[self.languages])
        self.assertTrue(self.skill_languages_2 in skill_query[self.languages])
        self.assertTrue(self.skill_languages_programming_1 in skill_query[self.languages_programming])
        self.assertTrue(self.skill_languages_programming_2 in skill_query[self.languages_programming])
        self.assertTrue(self.skill_as_a_person_1 in skill_query[self.as_a_person])
        self.assertTrue(self.skill_as_a_person_2 in skill_query[self.as_a_person])
        self.assertTrue(self.skill_as_a_person_3 in skill_query[self.as_a_person])


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
        response_profile_markdown = self.client.get(reverse("profile:profile_detail", args=[id, "md"]))
        response_profile_markdown_content = str(response_profile_markdown.content.decode("UTF-8"))

        self.assertEqual(response_jwt.status_code, status.HTTP_200_OK)
        self.assertEqual(response_profile_markdown.status_code, status.HTTP_200_OK)
        self.assertTrue(self.profile.email in response_profile_markdown_content )
        self.assertTrue(self.profile.first_name in response_profile_markdown_content)
        self.assertTrue(self.profile.last_name in response_profile_markdown_content)

        self.assertTrue(self.languages.name_category in response_profile_markdown_content)
        self.assertTrue(self.languages_programming.name_category in response_profile_markdown_content)
        self.assertTrue(self.as_a_person.name_category in response_profile_markdown_content)

        self.assertTrue(self.skill_languages_1.name in response_profile_markdown_content)
        self.assertTrue(self.skill_languages_2.name in response_profile_markdown_content)

        self.assertTrue(self.skill_languages_programming_1.name in response_profile_markdown_content)
        self.assertTrue(self.skill_languages_programming_2.name in response_profile_markdown_content)

        self.assertTrue(self.skill_as_a_person_1.name in response_profile_markdown_content)
        self.assertTrue(self.skill_as_a_person_2.name in response_profile_markdown_content)
        self.assertTrue(self.skill_as_a_person_3.name in response_profile_markdown_content)

    def test_url_profile_html_success(self):
        credentials = {
            'email': self.user_email,
            'password': self.user_password,
        }
        response_jwt = self.client.post(self.url_jwt, credentials)
        content = ast.literal_eval(response_jwt.content.decode("UTF-8"))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + content["access"])
        id = str(self.profile.id)
        response_profile_html = self.client.get(reverse("profile:profile_detail", args=[id, "html"]))

        response_profile_html_content = str(response_profile_html.content.decode("UTF-8"))

        self.assertEqual(response_jwt.status_code, status.HTTP_200_OK)
        self.assertEqual(response_profile_html.status_code, status.HTTP_200_OK)
        self.assertTrue(self.profile.email in response_profile_html_content)
        self.assertTrue(self.profile.first_name in response_profile_html_content)
        self.assertTrue(self.profile.last_name in response_profile_html_content)


        self.assertTrue(self.languages.name_category in response_profile_html_content)
        self.assertTrue(self.languages_programming.name_category in response_profile_html_content)
        self.assertTrue(self.as_a_person.name_category in response_profile_html_content)

        self.assertTrue(self.skill_languages_1.name in response_profile_html_content)
        self.assertTrue(self.skill_languages_2.name in response_profile_html_content)

        self.assertTrue(self.skill_languages_programming_1.name in response_profile_html_content)
        self.assertTrue(self.skill_languages_programming_2.name in response_profile_html_content)

        self.assertTrue(self.skill_as_a_person_1.name in response_profile_html_content)
        self.assertTrue(self.skill_as_a_person_2.name in response_profile_html_content)
        self.assertTrue(self.skill_as_a_person_3.name in response_profile_html_content)

    def test_url_profile_pdf_success(self):
        credentials = {
            'email': self.user_email,
            'password': self.user_password,
        }
        response_jwt = self.client.post(self.url_jwt, credentials)
        content = ast.literal_eval(response_jwt.content.decode("UTF-8"))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + content["access"])
        id = str(self.profile.id)
        response_profile_html = self.client.get(reverse("profile:profile_detail", args=[id, "pdf"]))

        self.assertEqual(response_jwt.status_code, status.HTTP_200_OK)
        self.assertEqual(response_profile_html.status_code, status.HTTP_200_OK)


    def test_url_profile_markdown_401_unauthorized_without_jwt(self):
        id = str(self.profile.id)
        response_profile_markdown = self.client.get(reverse("profile:profile_detail", args=[id, "md"]))
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
        response_profile_markdown = self.client.get(reverse("profile:profile_detail", args=[id, "md"]))
        self.assertEqual(response_profile_markdown.status_code, status.HTTP_404_NOT_FOUND)

    def test_url_profile_html_401_unauthorized_without_jwt(self):
        id = str(self.profile.id)
        response_profile_markdown = self.client.get(reverse("profile:profile_detail", args=[id, "html"]))
        self.assertEqual(response_profile_markdown.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_url_profile_html_404_not_found(self):
        credentials = {
            'email': self.user_email,
            'password': self.user_password,
        }
        response_jwt = self.client.post(self.url_jwt, credentials, format="json")
        content = ast.literal_eval(response_jwt.content.decode("UTF-8"))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + content["access"])
        id = '12312312h123h123211vf2_123'
        response_profile_markdown = self.client.get(reverse("profile:profile_detail", args=[id, "html"]))
        self.assertEqual(response_profile_markdown.status_code, status.HTTP_404_NOT_FOUND)


    def test_url_profile_pdf_401_unauthorized_without_jwt(self):
        id = str(self.profile.id)
        response_profile_markdown = self.client.get(reverse("profile:profile_detail", args=[id, "pdf"]))
        self.assertEqual(response_profile_markdown.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_url_profile_pdf_404_not_found(self):
        credentials = {
            'email': self.user_email,
            'password': self.user_password,
        }
        response_jwt = self.client.post(self.url_jwt, credentials, format="json")
        content = ast.literal_eval(response_jwt.content.decode("UTF-8"))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + content["access"])
        id = '12312312h123h123211vf2_123'
        response_profile_markdown = self.client.get(reverse("profile:profile_detail", args=[id, "pdf"]))
        self.assertEqual(response_profile_markdown.status_code, status.HTTP_404_NOT_FOUND)