from rest_framework import generics
from .models import Project, Category, ProjectPicture, Tag
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render


def add_project_images(request, images, project):
    user=isLogin(request)
    for image in images:
        data = ({ "project": project.id,"image": image })
        serializer = ProjectPictureSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"success": True, "message": "pictures added successfully"}, status=status.HTTP_201_CREATED)


def add_project_tags(request, tags, project):
    user=isLogin(request)
    print(tags)
    for tag in tags:
        data = ({
            "project": project.id,
            "tag": tag,
        })
        serializer = TagSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({"success": False,"errors": serializer.errors}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"success": True, "message": "tag added successfully"}, status=status.HTTP_201_CREATED)


class ProjectsView(APIView):
    def post(self, request, format=None):
        user=isLogin(request)
        project_data = request.data.copy()
        project_data['user'] = user.id
        if not request.FILES.getlist('pictures'):
            serializer = ({
            "success": False,
            "errors": {
                "pictures": "This field is required"
            }
        })
            return Response(serializer, status=status.HTTP_404_NOT_FOUND)
        if not request.POST.getlist('tags'):
            return Response({"success": False, "errors": {"tags": "This field is required"}}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(data=project_data)
        if serializer.is_valid():
            project = serializer.save()
            print(project.id)
            add_project_images(request, request.FILES.getlist('pictures'), project)
            add_project_tags(request, request.POST.getlist('tags'), project)

            return Response({"success": True,"message": "Project created successfully","date": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_404_NOT_FOUND)

    def get(self,request):
       user = isLogin(request)
       all= Project.objects.filter(user=user)
       serializer= ProjectSerializer(all, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)

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



class ProjectComments(APIView):
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True,"message": "comment created successfully","date": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": False,"errors": serializer.errors}, status=status.HTTP_404_NOT_FOUND)
