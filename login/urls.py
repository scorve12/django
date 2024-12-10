from django.contrib import admin
from django.urls import path
from login.views.login import LoginAPI, UserRegistrationAPI, KakaoLoginAPI

urlpatterns = [
    path('admin/', admin.site.urls),     
    path('login/', LoginAPI.as_view(), name='login'),  
    path('register/', UserRegistrationAPI.as_view(), name='user-register'),
    path('kakao/login/', KakaoLoginAPI.as_view(), name='kakao-login'),
]
