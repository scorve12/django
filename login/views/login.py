import requests
from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from login.serializers import UserRegistrationSerializer

from login.utils.kakao import get_kakao_user_info, get_or_create_user, generate_tokens_for_user

User = get_user_model()

class LoginAPI(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'username': username,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error', 'message': '로그인에 실패했습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        
class UserRegistrationAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "로그인에 성공했습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class KakaoLoginAPI(APIView):
    def post(self, request, *args, **kwargs):
        access_token = request.data.get("access_token")
        if not access_token:
            return Response({"error": "Access token이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        kakao_user_info = get_kakao_user_info(access_token)
        if not kakao_user_info:
            return Response({"error": "올바르지 않은 Kakao유저입니다."}, status=status.HTTP_400_BAD_REQUEST)

        user, created = get_or_create_user(kakao_user_info)

        tokens = generate_tokens_for_user(user)

        return Response({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "nickname": user.first_name,
            },
            "tokens": tokens,
        }, status=status.HTTP_200_OK)
