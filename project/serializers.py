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

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Comments
        fields = "__all__"



class ProjectSerializer(serializers.ModelSerializer):

    pictures = ProjectPictureSerializer(many=True, read_only=True, allow_null=True, required=False)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True, allow_null=True)
    user = UserSerializer(read_only=True)
    comments = CommentSerializer(many = True, allow_null=True)
    class Meta:
        model = Project
        fields = ['id', 'user', 'title', 'details', 'tags', 'category', 'total_target', 'pictures', 'start_time', 'end_time', 'comments']


class AddProjectSerialzer(serializers.ModelSerializer):
    pictures = ProjectPictureSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ['id', 'user', 'title', 'details', 'tag', 'category', 'total_target', 'pictures', 'start_time', 'end_time']




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











