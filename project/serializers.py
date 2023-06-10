from rest_framework import serializers

from user.serializers import UserSerializer
from .models import Donations, Project, Category, ProjectPicture, Tag, Comments
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


class ProjectSerializer(serializers.ModelSerializer):

    pictures = ProjectPictureSerializer(many=True, read_only=True, allow_null=True, required=False)
    category = CategorySerializer(read_only=True)
    tag = TagSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'user', 'title', 'details', 'tag', 'category', 'total_target', 'pictures', 'start_time', 'end_time']


class AddProjectSerialzer(serializers.ModelSerializer):
    pictures = ProjectPictureSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ['id', 'user', 'title', 'details', 'tag', 'category', 'total_target', 'pictures', 'start_time', 'end_time']



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"


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
















