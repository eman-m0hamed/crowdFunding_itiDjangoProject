from rest_framework import generics
from .models import Project, Category
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import *
from user.views import isLogin
from django.db.models import Sum
from django.utils import timezone


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
        cat = Category.objects.filter(id=request.data['category']).first()
        if not cat:
            return Response({"success": False, "errors": {"category":"category doesn't exist"}}, status=status.HTTP_400_BAD_REQUEST)
        project_data['category'] = cat.id
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

        serializer = AddProjectSerialzer(data=project_data)
        if serializer.is_valid(raise_exception=False):
            project = serializer.save()
            # print(project.id)

            add_project_images(request, request.FILES.getlist('pictures'), project)
            add_project_tags(request, request.POST.getlist('tags'), project)

            return Response({"success": True,"message": "Project created successfully","date": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = isLogin(request)
        allProjects = Project.objects.all()
        serializer = ProjectSerializer(allProjects, many=True)
        images_list = []
        for project in allProjects:
            images = [request.build_absolute_uri(image.image.url) for image in project.project_pictures.all()]
            images_list.append(images)

        # add the list of image URLs to the serializer data
        serializer_data = serializer.data
        for i, project_data in enumerate(serializer_data):
            project_data['pictures'] = images_list[i]
        return Response({"success": True, "data": serializer_data, "message": "All Your Projects are retrieved"})



class ProjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetails(APIView):
    def get(self, request, id):
        user = isLogin(request)
        project = Project.objects.filter(id=id).first()
        images = [request.build_absolute_uri(image.image.url) for image in project.project_pictures.all()]
        projectComments = Comments.objects.filter(project = project)
        comments = CommentSerializer(projectComments, many=True).data
        projectTags = Tag.objects.filter(project = project)
        tags = TagSerializer(projectTags, many=True).data
        if project:
            serializer = ProjectSerializer(project)
            ProjectDetails = serializer.data
            ProjectDetails['pictures'] = images
            ProjectDetails['comments'] = comments
            ProjectDetails['tags'] = tags
            return Response({"success": True, "data": ProjectDetails, "message": "project data is retrieved"})
        else:
            return Response({"success": False, "message": "projectnot found"})


    def delete(self, request, id):
        user = isLogin(request)
        project = Project.objects.filter(id=id).first()
        if project:
            if project.user != user:
                return Response({"success": False, "message": "You don't have access"}, status=status.HTTP_403_FORBIDDEN)
            allDonations = Donations.objects.filter(project=id).aggregate(Sum('money'))['money__sum'] or 0
            if allDonations > project.total_target*0.25:
                return Response({"success": False, "message": "You can't delete this project because project target exceeded '25%' of target"}, status=status.HTTP_400_BAD_REQUEST)

            project.delete()
            return Response({"success": True, "message": "Project Deleted Successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "message": "Project not found"}, status=status.HTTP_400_BAD_REQUEST)


class ProjectComments(APIView):
    def post(self, request, id):
        user = isLogin(request)
        project = Project.objects.filter(id=id).first()
        if project:
            comment_data = request.data.copy()
            comment_data['user'] = user.id
            comment_data['project'] = id
            serializer = AddCommentSerializer(data=comment_data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return Response({"success": True,"message": "comment created successfully","date": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"success": False,"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"success": False, "message": "projectnot found"})

    def get(self, request, id):
        user = isLogin(request)
        project = Project.objects.filter(id=id).first()
        if project:
            projectComments = Comments.objects.filter(project=id)
            serializer = CommentSerializer(projectComments, many=True)
            return Response({"success": True,"message": "all comments of project retrieved","date": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "message": "project not found"})


class DonationsView(APIView):
    def post(self, request, id):
        user = isLogin(request)
        project = Project.objects.filter(id=id).first()
        if project:
            donation_data = request.data.copy()
            donation_data['user'] = user.id
            donation_data['project']=id
            serializer = AddDonationSerializer(data=donation_data)
            if serializer.is_valid(raise_exception=False):
                allDonations = Donations.objects.filter(project=id).aggregate(Sum('money'))['money__sum'] or 0
                if allDonations >= project.total_target or timezone.now() > project.end_time:
                    return Response({"success": False,"message": "project already arrived to its target"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer.save()
                    project.donation=allDonations+int(donation_data['money'])
                    project.save()
                    return Response({"success": True,"message": "Donation Send Successfully","date": serializer.data}, status=status.HTTP_200_OK)

            else:
                return Response({"success": False,"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"success": False,"message": "project not found"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        user = isLogin(request)
        project = Project.objects.filter(id=id).first()
        if project.user != user:
             return Response({"success": False, "message": "You don't have access"}, status=status.HTTP_403_FORBIDDEN)
        if project:
            projectDonations = Donations.objects.filter(project=id);
            selializer = DonationSerializer(projectDonations, many= True)
            return Response({"success": True, "data": selializer.data, "message": "all donations of project retrieved"})

        else:
            return Response({"success": False, "message": "Project not found"}, status=status.HTTP_400_BAD_REQUEST)

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryProjects(APIView):
    def get(self, request, id):
        user = isLogin(request)
        category = Category.objects.filter(id=id).first()

        if category:
            categorySerializer = CategorySerializer(category)
            categoryProjects = Project.objects.filter(category=category)
            projectSerializer = ProjectSerializer(categoryProjects, many=True)
            serialized_data = categorySerializer.data
            serialized_data['project'] = projectSerializer.data
            return Response({"success": True, "data": serialized_data,"message": "category data retrieved"})
        else:
            return Response({"success": False, "message": "category not found"})


class LastFiveProjects(APIView):
    def get(self, request):
        user= isLogin(request)

        projects= Project.objects.all().order_by('-created_at')[:5]
        serializer = ProjectSerializer(projects, many=True);
        images_list = []
        for project in projects:
            images = [request.build_absolute_uri(image.image.url) for image in project.project_pictures.all()]
            images_list.append(images)

        # add the list of image URLs to the serializer data
        serializer_data = serializer.data
        for i, project_data in enumerate(serializer_data):
            project_data['pictures'] = images_list[i]
        return Response({"success": True, "data": serializer_data, "message": "Last 5 Projects are retrieved"})
