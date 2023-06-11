from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Project)
admin.site.register(Comments)
admin.site.register(ProjectReport)
admin.site.register(CommentReport)

