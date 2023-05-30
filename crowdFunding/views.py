from rest_framework import generics
from .models import myUser, Project, Category, ProjectPicture, Tag
from .serializers import *
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime

class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = myUser.objects.all()
    serializer_class = UserSerializer

class UserLoginView(generics.GenericAPIView, CreateModelMixin):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        if 'email' not in request.data and 'password' not in request.data:
          return Response({"errors": {"email": ["this field is required"], "password": ["this field is required"]}}, status=status.HTTP_400_BAD_REQUEST)
    
        elif 'email' not in request.data:
            return Response({"errors": {"email": ["this field is required"]}}, status=status.HTTP_400_BAD_REQUEST)
        
        elif 'password' not in request.data:
            return Response({"errors": {"password": ["this field is required"]}}, status=status.HTTP_400_BAD_REQUEST)
    
        user = myUser.objects.filter(email=request.data['email']).first()

        if user is None:
            raise AuthenticationFailed('user Account not found!')

        if not user.check_password(request.data['password']):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.data = {
        'token': token,
        'login': True
        }
        return response

class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = myUser.objects.all()
    serializer_class = UserSerializer


class ProjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProjectPictureListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProjectPicture.objects.all()
    serializer_class = ProjectPictureSerializer


class ProjectPictureRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectPicture.objects.all()
    serializer_class = ProjectPictureSerializer


class TagListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    

class UserProjectListAPIView(APIView):
    def get(self, request, user_id):
        user = myUser.objects.get(pk=user_id)
        projects = Project.objects.filter(user=user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)