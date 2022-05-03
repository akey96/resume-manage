from profiles.views import ProfileAPIViewMD
from django.urls import path

app_name = 'profile'

urlpatterns = [
        path('<slug:pk>.md', ProfileAPIViewMD.as_view(), name='profile_md'),
 ]