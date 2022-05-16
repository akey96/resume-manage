from profiles.views import ProfileAPIView
from django.urls import path, re_path
from profiles.views import ProfileListAPIView

app_name = 'profile'

urlpatterns = [
        re_path('(?P<pk>[\w-]+)\.(md|html|pdf)', ProfileAPIView.as_view(), name='profile_detail'),
        path('profile', ProfileListAPIView.as_view(), name='profile_detail'),
]