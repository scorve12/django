import requests
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

def get_kakao_user_info(access_token):
    url = "https://kapi.kakao.com/v2/user/me"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  # 사용자 정보 반환
    else:
        return None

User = get_user_model()

def get_or_create_user(kakao_user_info):
    kakao_id = kakao_user_info.get("id")
    nickname = kakao_user_info.get("properties", {}).get("nickname")
    email = kakao_user_info.get("kakao_account", {}).get("email")

    # 카카오 ID를 기반으로 사용자 조회 또는 생성
    user, created = User.objects.get_or_create(
        username=f"kakao_{kakao_id}",
        defaults={
            "first_name": nickname,
            "email": email,
        }
    )
    return user, created


def generate_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

