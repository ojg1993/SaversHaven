from django.conf import settings
from django.shortcuts import redirect
from core.models import User
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse
import requests
from rest_framework import status
from json.decoder import JSONDecodeError

from rest_framework.response import Response


BASE_URL = 'http://localhost:8000/api/auth/'
GOOGLE_CALLBACK_URI = BASE_URL + 'google/login/callback/'

state = getattr(settings, "STATE")
client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
client_secret = getattr(settings, "SOCIAL_AUTH_GOOGLE_SECRET")

def google_login(request):
    scope = "https://www.googleapis.com/auth/userinfo.email"

    # Code Request
    return redirect(
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")


def google_callback(request):
    code = request.GET.get('code')

    # 1. Access Token Request
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
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

        # 3-1. if social account doesn't exist, return error
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'},
                                status=status.HTTP_400_BAD_REQUEST)
        # 3-1. if social account's provide doesn't match, return error
        if social_user.provider != 'google':
            return JsonResponse({'err_msg': 'no matching social type'},
                                status=status.HTTP_400_BAD_REQUEST)

        # 3-2 if not above proceed to logging in and issuing JWT token
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}google/login/finish/", data=data)
        accept_status = accept.status_code

        # 3-2. error handling while authentication
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to login'},
                                status=accept_status)

        accept_json = accept.json()
        accept_json.pop('user', None)

        return JsonResponse(accept_json)

    # 3. Proceed registration with the given email, access token & code
    except User.DoesNotExist:
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}/google/login/finish/", data=data)
        accept_status = accept.status_code

        # 3-1. error handling while registration
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'},
                                status=accept_status)

        accept_json = accept.json()
        accept_json.pop('user', None)

        return JsonResponse(accept_json)

    # 4. None Social user email
    except SocialAccount.DoesNotExist:
        return JsonResponse(
            {'err_msg': 'email exists but not a social registered user'},
            status=status.HTTP_400_BAD_REQUEST)


class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client
