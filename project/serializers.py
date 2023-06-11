from rest_framework import serializers

from user.serializers import UserSerializer
from .models import *
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProjectPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPicture
        fields = ['id', 'image', 'project']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'project']


class AddCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"


class AddReportProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectReport
        fields = "__all__"


class ReportProjectSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True, allow_null=True)
    class Meta:
        model = ProjectReport
        fields = "__all__"


class AddReportCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReport
        fields = "__all__"


class ReportCommentSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True, allow_null=True)
    class Meta:
        model = CommentReport
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, allow_null=True)
    reports = ReportCommentSerializer(read_only=True, allow_null=True)
    class Meta:
        model = Comments
        fields = ['id', 'project', 'user', 'reports']


class ProjectSerializer(serializers.ModelSerializer):

    pictures = ProjectPictureSerializer(many=True, read_only=True, allow_null=True, required=False)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True, allow_null=True)
    user = UserSerializer(read_only=True)
    comments = CommentSerializer(many = True, allow_null=True)
    reports = ReportProjectSerializer(many = True, allow_null=True)

    class Meta:
        model = Project
        fields = ['id', 'user', 'title', 'details', 'tags', 'category', 'total_target', 'pictures', 'start_time', 'end_time', 'comments' ,'donation', 'reports']


class AddProjectSerialzer(serializers.ModelSerializer):
    pictures = ProjectPictureSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True, allow_null=True)

    class Meta:
        model = Project
        fields = ['id', 'user', 'title', 'details', 'tags', 'category', 'total_target', 'pictures', 'start_time', 'end_time']


class AddDonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donations
        fields = "__all__"


class DonationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    project = ProjectSerializer()
    class Meta:
        model = Donations
        fields = "__all__"


class CategoryListSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    class Meta:
        model = Category
        fields = ['id', 'name', 'project']




