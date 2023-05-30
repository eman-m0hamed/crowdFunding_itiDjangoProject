from rest_framework import serializers
from .models import myUser, Project, Category, ProjectPicture, Tag
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



class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=myUser.objects.all())  
    class Meta:
        model = Project
        fields = ['id', 'user', 'title', 'details', 'category', 'pictures', 'total_target', 'tags', 'start_time', 'end_time']



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProjectPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPicture
        fields = ['id', 'image','project']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        

class UserLoginSerializer(serializers.ModelSerializer):
      class Meta:
        model=myUser
        fields=['email','password']

        
        
        
        
        
        
        



    
    
    
    
    
    
    
    
