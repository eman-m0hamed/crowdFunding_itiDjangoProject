from rest_framework import serializers
from .models import Project, Category, ProjectPicture, Tag, Comments
from rest_framework import serializers


class ProjectPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPicture
        fields = ['id', 'image', 'project']


class ProjectSerializer(serializers.ModelSerializer):

    pictures = ProjectPictureSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'user', 'title', 'details', 'category', 'total_target', 'pictures', 'start_time', 'end_time']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"
















