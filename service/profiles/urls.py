from profiles.views import ProfileAPIView
from django.urls import path, re_path

app_name = 'profile'

urlpatterns = [
        re_path('(?P<pk>[\w-]+)\.(md|html)', ProfileAPIView.as_view(), name='profile_detail'),
]