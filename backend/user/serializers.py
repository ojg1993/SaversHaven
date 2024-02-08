from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.account import app_settings as allauth_account_settings
from allauth.socialaccount.models import EmailAddress



class UserSerializer(serializers.ModelSerializer):
    username = None
    class Meta:
        model = get_user_model()
        fields = (
            'email', 'password', 'nickname',
            'first_name', 'last_name', 'phone_number'
        )
        extra_kwargs = {'password': {'write_only': True, 'min_length': 10}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class TokenLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _('Unable to log in with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')
        attrs['user'] = user
        return attrs

class CustomRegisterSerializer(RegisterSerializer):
    username = None
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    nickname = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_account_settings.UNIQUE_EMAIL:
            if email and EmailAddress.objects.filter(email=email, verified=True).exists():
                raise serializers.ValidationError(
                    _('A user is already registered with this e-mail address.'),
                )
        return email

    def get_cleaned_data(self):
        super().get_cleaned_data()
        return {
            "email": self.validated_data.get('email', ""),
            "password1": self.validated_data.get('password1', ""),
            "nickname": self.validated_data.get('nickname', ""),
            "first_name": self.validated_data.get('first_name', ""),
            "last_name": self.validated_data.get('last_name', ""),
            "phone_number": self.validated_data.get('phone_number')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self)
        user.save()

        setup_user_email(request, user, [])
        user.email = self.cleaned_data.get('email')
        user.password = self.cleaned_data.get('password1')
        user.nickname = self.cleaned_data.get('nickname')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_number = self.cleaned_data.get('phone_number')