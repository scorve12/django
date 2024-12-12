from django.shortcuts import redirect
from django.conf import settings

def kakao_login(request):
    client_id = settings.KAKAO_REST_API_KEY
    redirect_uri = "http://https://gotrip-iota.vercel.app/"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )
    
def get_kakao_user_info(access_token):
    import requests
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://kapi.kakao.com/v2/user/me", headers=headers)
    if response.status_code != 200:
        return None
    return response.json()

def get_or_create_user(kakao_user_info):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    email = kakao_user_info['kakao_account'].get('email')
    user, created = User.objects.get_or_create(email=email, defaults={
        'username': kakao_user_info.get('id'),
        'first_name': kakao_user_info['properties'].get('nickname', '')
    })
    return user, created

def generate_tokens_for_user(user):
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }