from rest_framework import generics
from .models import Project, Category
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import *
from user.views import isLogin
from django.db.models import Sum, Avg
from django.utils import timezone


def add_project_images(request, images, project):
    user=isLogin(request)
    for image in images:
        data = ({ "project": project.id,"image": image })
        serializer = ProjectPictureSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
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
            "project": project.id,
            "name": tag,
        })

        serializer = TagSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            print(data)
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

        serializer_data = serializer.data
        for i, project_data in enumerate(serializer_data):
            project_data['pictures'] = images_list[i]
            projectComments = Comments.objects.filter(project = project_data['id'])
            projectTags = Tag.objects.filter(project = project_data['id'])
            projectReports = ProjectReport.objects.filter(project=project_data['id'])
            comments = CommentSerializer(projectComments, many=True).data
            tags = TagSerializer(projectTags, many=True).data
            reports = ReportProjectSerializer(projectReports, many=True).data
            project_data['comments'] = comments
            project_data['tags'] = tags
            project_data['reports'] = reports
        return Response({"success": True, "data": serializer_data, "message": "All Your Projects are retrieved"})


class ProjectDetails(APIView):
    def get(self, request, id):
        user = isLogin(request)
        project = Project.objects.filter(id=id).first()
        images = [request.build_absolute_uri(image.image.url) for image in project.project_pictures.all()]
        projectComments = Comments.objects.filter(project = project)
        projectTags = Tag.objects.filter(project = project)
        projectReports = ProjectReport.objects.filter(project=id)
        comments = CommentSerializer(projectComments, many=True).data
        tags = TagSerializer(projectTags, many=True).data
        reports = ReportProjectSerializer(projectReports, many=True).data
        if project:
            serializer = ProjectSerializer(project)
            ProjectDetails = serializer.data
            ProjectDetails['pictures'] = images
            ProjectDetails['comments'] = comments
            ProjectDetails['tags'] = tags
            ProjectDetails['reports'] = reports
            return Response({"success": True, "data": ProjectDetails, "message": "project data is retrieved"})
        else:
            return Response({"success": False, "message": "projectnot found"}, status=status.HTTP_400_BAD_REQUEST )


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
            return Response({"success": False, "message": "project not found"}, status=status.HTTP_400_BAD_REQUEST)

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
            images_list = []
            for project in categoryProjects:
                images = [request.build_absolute_uri(image.image.url) for image in project.project_pictures.all()]
                images_list.append(images)

            projects_data = projectSerializer.data
            for i, project in enumerate(projects_data):
                project['pictures'] = images_list[i]

            category_data = categorySerializer.data
            category_data['project'] = projectSerializer.data
            return Response({"success": True, "data": category_data,"message": "category data retrieved"})
        else:
            return Response({"success": False, "message": "category not found"}, status=status.HTTP_400_BAD_REQUEST)


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


class ReportProject(APIView):
    def post(self, request, id):
        user = isLogin(request)
        project = Project.objects.filter(id=id).first()
        if not project:
            return Response({"success": False, "message": "Project not found"}, status=status.HTTP_400_BAD_REQUEST)

        report_data = request.data.copy()
        report_data['user'] = user.id
        report_data['project'] = id
        serializer = AddReportProjectSerializer(data= report_data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response({"success": True,"message": "Report Send Successfully","date": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False,"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        user = isLogin(request)

        project = ProjectReport.objects.filter(project=id)
        if not project:
            return Response({"success": False, "message": "Project not found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ReportProjectSerializer(project, many=True)
        return Response({"success": True, "data": serializer.data, "message": "project reports"})


class ReportComment(APIView):
    def post(self, request, *args, **kwargs):
        user = isLogin(request)
        projectId = kwargs['projectId']
        commentId = kwargs['id']
        comment = Comments.objects.filter(id=commentId, project= projectId).first()
        if not comment:
            return Response({"success": False, "message": "comment not found"}, status=status.HTTP_400_BAD_REQUEST)

        report_data = request.data.copy()
        report_data['user'] = user.id
        report_data['comment'] = commentId
        serializer = AddReportCommentSerializer(data= report_data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response({"success": True,"message": "Report Send Successfully","date": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False,"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request,  *args, **kwargs):
        user = isLogin(request)
        projectId = kwargs['projectId']
        commentId = kwargs['id']
        projectComments = CommentReport.objects.filter(comment = commentId)
        if not projectComments:
            return Response({"success": False, "message": "comment not found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ReportCommentSerializer(projectComments, many=True)
        return Response({"success": True, "data": serializer.data, "message": "project reports"})


class TagsView(APIView):
    def get(self, request):
        user = isLogin(request)
        allTags = Tag.objects.all()
        serializer = TagSerializer(allTags, many=True)
        return Response ({"success": True, "data": serializer.data, "message": "all tags are retrieved"}, status=status.HTTP_200_OK)



class RateProject(APIView):
    def post(self, request, id):
        user = isLogin(request)
        project = Project.objects.filter(id=id).first()
        if not project:
            return Response({"success": False, "message": "Project not found"}, status=status.HTTP_400_BAD_REQUEST)

        rate_data = request.data.copy()
        rate_data['user'] = user.id
        rate_data['project'] = id
        serializer = AddProjectRateSerializer(data= rate_data)
        if serializer.is_valid(raise_exception=False):
            project_rates = ProjectRate.objects.filter(project=project)
            overall_rate = project_rates.aggregate(Avg('rate'))['rate__avg']
            project.averageRate = overall_rate + int(rate_data['rate'])
            serializer.save()
            project.save()
            return Response({"success": True,"message": "rate done Successfully","date": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False,"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class  HighestFiveRated(APIView):
    def get(self, request):
        user= isLogin(request)

        projects= Project.objects.all().order_by('averageRate')[:5]
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


class  lastFiveProjectSelectedByAdmin(APIView):
    def get(self, request):
        user= isLogin(request)

        projects= Project.objects.filter(is_selected_by_admin=True).reverse()[:5]
        serializer = ProjectSerializer(projects, many=True);
        images_list = []
        for project in projects:
            images = [request.build_absolute_uri(image.image.url) for image in project.project_pictures.all()]
            images_list.append(images)

        # add the list of image URLs to the serializer data
        serializer_data = serializer.data
        for i, project_data in enumerate(serializer_data):
            project_data['pictures'] = images_list[i]
        return Response({"success": True, "data": serializer_data, "message": "Last 5 Projects selected by admin are retrieved"})

