from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    username = None
    class Meta:
        model = get_user_model()
        fields = (
            'email', 'password', 'nickname',
            'first_name', 'last_name', 'phone_number'
        )
        extra_kwargs = {'password': {'write_only': True, 'min_length': 10}}

class CustomRegisterSerializer(RegisterSerializer):
    username = None
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    nickname = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)

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
        user.nickname = self.cleaned_data.get('nickname')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_number = self.cleaned_data.get('phone_number')

        adapter.clean_password(self.cleaned_data['password1'], user=user)
        return user
