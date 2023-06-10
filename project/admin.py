from django.contrib import admin
from .models import Category, Tag, Project, ProjectPicture

# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Project)
admin.site.register(ProjectPicture)
