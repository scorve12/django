from django.contrib import admin
from django.urls import path, include
from login.views.login import LoginAPI, UserRegistrationAPI, kakao_login, kakao_callback

urlpatterns = [
    path('admin/', admin.site.urls),     
    path('login/', LoginAPI.as_view(), name='login'),  
    path('register/', UserRegistrationAPI.as_view(), name='user-register'),
    path('kakao/login/', kakao_login, name='kakao-login'),
    path('kakao/callback/', kakao_callback, name='kakao-callback'),
]
