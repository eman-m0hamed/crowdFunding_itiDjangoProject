from rest_framework import generics
from .models import Project, Category, ProjectPicture, Tag
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from user.models import *
from user.views import isLogin


def add_project_images(request, images, project):
    user=isLogin(request)
    for image in images:
        data = ({ "project": project.id,"image": image })
        serializer = ProjectPictureSerializer(data=data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
        else:
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"success": True, "message": "pictures added successfully"}, status=status.HTTP_200_OK)


def add_project_tags(request, tags, project):
    user=isLogin(request)
    print(tags)
    for tag in tags:
        data = ({
            "project": project,
            "tag": tag,
        })
        serializer = TagSerializer(data=data)
        if serializer.is_valid(raise_exception=False):
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
        project_data['category'] = Category.objects.filter(id=request.data['category']).first().id
        if not request.FILES.getlist('pictures'):
            serializer = ({
            "success": False,
            "errors": {
                "pictures": "This field is required"
            }
        })
            return Response(serializer, status=status.HTTP_400_BAD_REQUEST)

        if not request.POST.getlist('tags'):
            return Response({"success": False, "errors": {"tags": "This field is required"}}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProjectSerializer(data=project_data)
        if serializer.is_valid(raise_exception=False):
            project = serializer.save()
            # print(project.id)

            add_project_images(request, request.FILES.getlist('pictures'), project)
            add_project_tags(request, request.POST.getlist('tags'), project)

            return Response({"success": True,"message": "Project created successfully","date": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # def get(self,request):
    #    user = isLogin(request)
    #    all= Project.objects.filter(user=user)
    #    serializer= ProjectSerializer(all, many=True)
    #    return Response(serializer.data, status=status.HTTP_200_OK)


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
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response({"success": True,"message": "comment created successfully","date": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False,"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

