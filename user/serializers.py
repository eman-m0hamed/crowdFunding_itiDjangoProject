from rest_framework import serializers
from .models import myUser
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = myUser
        fields = ['id', 'email', 'first_name', 'last_name', 'mobile_phone', 'profile_picture', 'password']
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = myUser.objects.create_user(password=password, **validated_data)
        return user

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta():
        model = myUser
        fields = ['token']


class UserLoginSerializer(serializers.ModelSerializer):
      class Meta:
        model=myUser
        fields=['email','password']












