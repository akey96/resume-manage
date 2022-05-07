from django.http import HttpResponse
from django.shortcuts import render
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from profiles.models import Profile
import markdown2

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        try:
            queryset = Profile.objects.get(id=pk)            
            type_response = request.get_full_path().split('.')[1]
            if type_response == 'html':
                content_markdown = render(request, "profile_list.html", {"profile": queryset}).content
                return HttpResponse(markdown2.markdown(content_markdown), content_type='text/html')
            elif type_response == 'md':
                return HttpResponse(render(request, "profile_list.html", {"profile": queryset}).content, content_type='text/plain')
        except ValidationError:
            return Response({'error': "Acceso no autorizado"}, status=status.HTTP_404_NOT_FOUND)