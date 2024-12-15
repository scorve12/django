from django.contrib import admin
from django.urls import path, include
from login.views.login import LoginAPI, UserRegistrationAPI, kakao_login, kakao_callback, get_kakao_token
from login.views.gotrip import TripAPI
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/admin/', admin.site.urls),     
    path('api/login/', LoginAPI.as_view(), name='login'),  
    path('api/register/', UserRegistrationAPI.as_view(), name='user-register'),
    path('api/kakao/login/', kakao_login, name='kakao-login'),
    path('kakao/callback/', kakao_callback, name='kakao-callback'),
    path('api/kakao/token/', get_kakao_token, name='kakao-token'),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api/trip/', TripAPI.as_view(), name='trip'),
]
