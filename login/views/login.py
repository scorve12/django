import requests
from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from login.serializers import UserRegistrationSerializer
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from login.models import CustomUser
from rest_framework.permissions import AllowAny

User = get_user_model()

class LoginAPI(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # 사용자 인증
        user = authenticate(username=username, password=password)
        if user:
            # 토큰 발급
            refresh = RefreshToken.for_user(user)

            # 토큰 저장
            user.access_token = str(refresh.access_token)
            user.refresh_token = str(refresh)
            user.save()

            return Response({
                'status': 'success',
                'username': username,
                'access': user.access_token,
                'refresh': user.refresh_token,
            }, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error', 'message': '로그인에 실패했습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        

class UserRegistrationAPI(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입에 성공했습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def kakao_login(request):
    permission_classes = [AllowAny]
    client_id = settings.KAKAO_REST_API_KEY
    redirect_uri = settings.KAKAO_REDIRECT_URI
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )

def kakao_callback(request):
    permission_classes = [AllowAny]
    code = request.GET.get('code')

    frontend_redirect_url = f"https://capstone-sigma-sable.vercel.app/kakao/callback?code={code}"
    return redirect(frontend_redirect_url)

def get_kakao_token(request):
    permission_classes = [AllowAny]
    # 1. 전달받은 Authorization Code 가져오기
    code = request.GET.get('code')
    if not code:
        return JsonResponse({"error": "코드를 추가하세요"}, status=400)

    # 2. 카카오 서버로 액세스 토큰 요청
    token_request = requests.post(
        "https://kauth.kakao.com/oauth/token",
        data={
            "grant_type": "authorization_code",
            "client_id": settings.KAKAO_REST_API_KEY,
            "redirect_uri": settings.KAKAO_REDIRECT_URI,
            "code": code,
        },
    )
    token_response = token_request.json()

    # 3. 카카오 액세스 토큰 검증
    access_token = token_response.get('access_token')
    if not access_token:
        return JsonResponse({"error": "Failed to get access token."}, status=400)

    # 4. 카카오 사용자 정보 가져오기
    headers = {"Authorization": f"Bearer {access_token}"}
    profile_request = requests.get("https://kapi.kakao.com/v2/user/me", headers=headers)
    profile_response = profile_request.json()

    if profile_request.status_code != 200:
        return JsonResponse({"error": "Failed to fetch user profile."}, status=400)

    # 5. 사용자 정보 파싱
    kakao_account = profile_response.get('kakao_account', {})
    kakao_id = profile_response.get('id')
    email = kakao_account.get('email')
    gender = kakao_account.get('gender')
    age_range = kakao_account.get('age_range')
    nickname = kakao_account.get('profile', {}).get('nickname', '')

    # 6. 사용자 생성 또는 업데이트
    user, created = CustomUser.objects.update_or_create(
        kakao_id=kakao_id,
        defaults={
            'username': nickname,
            'email': email,
            'gender': '남' if gender == 'M' else '여' if gender == 'F' else None,
            'age': age_range,
        }
    )

    # 7. JWT 토큰 발급
    if user:
        # SimpleJWT 토큰 생성
        refresh = RefreshToken.for_user(user)

        # 사용자 모델에 카카오 액세스 토큰 저장 (선택적)
        user.access_token = access_token  # 카카오 토큰 저장
        user.save()

        # 응답 반환
        return JsonResponse({
            'status': 'success',
            'username': user.username,
            'access': str(refresh.access_token),  # JWT access_token
            'refresh': str(refresh),  # JWT refresh_token
        }, status=200)

    # 8. 사용자 생성 실패 시 처리
    return JsonResponse({
        'status': 'error',
        'message': '로그인에 실패했습니다.'
    }, status=401)

# def get_kakao_token(request):
#     code = request.POST.get('code')

#     # 카카오로 액세스 토큰 요청
#     token_request = requests.post(
#         "https://kauth.kakao.com/oauth/token",
#         data={
#             "grant_type": "authorization_code",
#             "client_id": settings.KAKAO_REST_API_KEY,
#             "redirect_uri": settings.KAKAO_REDIRECT_URI,
#             "code": code,
#         },
#     )
#     token_response_json = token_request.json()
#     return JsonResponse(token_response_json)
# def kakao_callback(request):
#     permission_classes = [AllowAny]
#     code = request.GET.get('code')
    
#     # 카카오 토큰 요청
#     token_request = requests.post(
#         "https://kauth.kakao.com/oauth/token",
#         data={
#             "grant_type": "authorization_code",
#             "client_id": settings.KAKAO_REST_API_KEY,
#             "redirect_uri": settings.KAKAO_REDIRECT_URI,
#             "code": code,
#         },
#     )
#     token_response_json = token_request.json()
#     access_token = token_response_json.get('access_token')
#     refresh_token = token_response_json.get('refresh_token')
    
#     # 카카오로부터 사용자 정보 가져오기
#     headers = {"Authorization": f"Bearer {access_token}"}
#     profile_request = requests.get("https://kapi.kakao.com/v2/user/me", headers=headers)
#     profile_json = profile_request.json()
    
#     # 사용자 정보 파싱
#     kakao_account = profile_json.get('kakao_account')
#     kakao_id = profile_json.get('id')
#     email = kakao_account.get('email')
#     gender = kakao_account.get('gender')
#     age_range = kakao_account.get('age_range')

#     # 사용자 생성 또는 업데이트
#     user, created = CustomUser.objects.update_or_create(
#         kakao_id=kakao_id,
#         defaults={
#             'username': kakao_account.get('profile', {}).get('nickname', ''),
#             'email': email,
#             'gender': '남' if gender == 'male' else '여' if gender == 'female' else None,
#             'age': age_range 
#         }
#     )

#     if user:
#         # 카카오에서 받은 토큰을 사용자 모델에 저장
#         refresh = RefreshToken.for_user(user)
        
#         user.access_token = refresh.access_token
#         user.refresh_token = refresh
#         user.save()

#         # SimpleJWT 토큰 발급
        

#         return JsonResponse({
#             'status': 'success',
#             'username': user.username,
#             #'access': user.access_token,  # 카카오 access_token
#             #'refresh': user.refresh_token,  # 카카오 refresh_token
#             'access': str(refresh.access_token),  # JWT access_token
#             'refresh': str(refresh),  # JWT refresh_token
#         }, status=status.HTTP_200_OK)
#     else:
#         return JsonResponse({
#             'status': 'error', 
#             'message': '로그인에 실패했습니다.'
#         }, status=status.HTTP_401_UNAUTHORIZED)


class UserprofileAPI(APIView):
    def get(self, request, id):
        user = request.user      
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }, status=status.HTTP_200_OK)
