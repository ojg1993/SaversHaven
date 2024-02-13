from json.decoder import JSONDecodeError

import requests
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from core.models import User

BASE_URL = 'http://localhost:8000/api/auth/'
GOOGLE_CALLBACK_URI = BASE_URL + 'google/login/callback/'

state = getattr(settings, "STATE")
client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
client_secret = getattr(settings, "SOCIAL_AUTH_GOOGLE_SECRET")


def google_login(request):
    scope = "https://www.googleapis.com/auth/userinfo.email"

    # Code Request
    return redirect(
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&"
        f"response_type=code&"
        f"redirect_uri={GOOGLE_CALLBACK_URI}&"
        f"scope={scope}")


def google_callback(request):
    code = request.GET.get('code')

    # 1. Access Token Request
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&"
        f"client_secret={client_secret}&"
        f"code={code}&"
        f"grant_type=authorization_code&"
        f"redirect_uri={GOOGLE_CALLBACK_URI}&"
        f"state={state}")
    # 1-1. json transformation & error parsing
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    # 1-2 if an error occurs raise
    if error is not None:
        raise JSONDecodeError(error)

    # 1-3. if no error, retrieve access token
    access_token = token_req_json.get('access_token')

    # 2. Email request to google with the access token
    email_req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code

    # 2-1. if error occurs 400 return
    if email_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'},
                            status=status.HTTP_400_BAD_REQUEST)

    # 2-2. if no error, retrieve email
    email_req_json = email_req.json()
    email = email_req_json.get('email')

    # 3. Proceed login with email, access token and code
    try:
        # 3-1. Query if a user with given email exists
        user = User.objects.get(email=email)
        social_user = SocialAccount.objects.get(user=user)

        # if social account doesn't exist, return error
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'},
                                status=status.HTTP_400_BAD_REQUEST)
        # if social account's provide doesn't match, return error
        if social_user.provider != 'google':
            return JsonResponse({'err_msg': 'no matching social type'},
                                status=status.HTTP_400_BAD_REQUEST)

        # 3-2 if not above proceed to logging in and issuing JWT token
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}google/login/finish/", data=data)

        # if error occurs, return error
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to login with google'},
                                status=accept_status)

        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)

        return JsonResponse(
            {"access token": str(access_token),
             "refresh token": str(refresh_token)
             }
        )

    # 3. Proceed registration with the given email, access token & code
    except User.DoesNotExist:
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}google/login/finish/", data=data)
        accept_status = accept.status_code

        # 3-1. error handling while registration
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup with google'},
                                status=accept_status)

        user = User.objects.get(email=email)
        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)

        return JsonResponse(
            {"access token": str(access_token),
             "refresh token": str(refresh_token)
             }
        )

    # 4. None Social user email
    except SocialAccount.DoesNotExist:
        return JsonResponse(
            {'err_msg': 'email exists but not a google user'},
            status=status.HTTP_400_BAD_REQUEST)


class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client


class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        # 사용자가 이메일 확인 링크로 GET 요청을 보낼 때 실행되는 메서드
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        return HttpResponseRedirect("/")  # 인증실패 / 인증성공
        # 이메일 확인 객체를 가져오고, 해당 객체의 confirm 메서드를 호출하여 이메일을 확인

    def get_object(self, queryset=None):
        # URL에서 추출한 이메일 확인 키를 사용하여 EmailConfirmationHMAC.from_key를 호출하여 이메일 확인 객체를 가져옴
        key = self.kwargs["key"]
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                email_confirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                return HttpResponseRedirect("/")  # 인증실패 # 인증실패
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        # 모든 유효한 이메일 확인 객체를 반환하는 쿼리셋을 정의
        qs = qs.select_related("email_address__user")
        # 연결된 이메일 주소 및 사용자 정보를 함께 가져움
        return qs
