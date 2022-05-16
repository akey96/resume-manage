from django.http import HttpResponse
from django.shortcuts import render
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from profiles.models import Profile, CategorySkill, Skill
import markdown2
from .utils import PDFUtils
from profiles.serializers import ProfileSerializer

class ProfileListAPIView(ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(state=True)

class ProfileAPIView(APIView):
        
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        try:
            profile_query = Profile.objects.get(id=pk)
            category_skill_query = CategorySkill.objects.filter(profile=profile_query)
            skill_query = {}
            for cat in category_skill_query:
                skill_query[cat] = Skill.objects.filter(category_skill=cat)
            type_response = request.get_full_path().split('.')[1]
            if type_response == 'html':
                content_markdown = render(request, "profile_markdown.md", {"profile": profile_query, 'skill_query': skill_query}).content
                return HttpResponse(markdown2.markdown(content_markdown), content_type='text/html')
            elif type_response == 'md':
                return HttpResponse(render(request, "profile_markdown.md", {"profile": profile_query, 'skill_query': skill_query}).content, content_type='text/plain')
            elif type_response == 'pdf':
                pdf = PDFUtils.html_to_pdf('profile_html', {"profile": profile_query, 'skill_query': skill_query})
                return HttpResponse(pdf, content_type='application/pdf')
        except ValidationError:
            return Response({'error': "Acceso no autorizado"}, status=status.HTTP_404_NOT_FOUND)