from django.http import HttpResponse
from django.shortcuts import render
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from profiles.models import Profile
import markdown2

class ProfileAPIViewMD(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        try:
            queryset = Profile.objects.get(id=pk)
            return HttpResponse(render(request, "profile_list.html", {"profile": queryset}).content, content_type='text/plain')
        except ValidationError:
            return Response({'error': "Acceso no autorizado"}, status=status.HTTP_404_NOT_FOUND)
