from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from account import serializers


class RegisterView(generics.CreateAPIView):
    '''Register a new user'''
    serializer_class = serializers.UserSerializer


class TokenLoginView(ObtainAuthToken):
    '''Create Token upon login'''
    serializer_class = serializers.TokenLoginSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
