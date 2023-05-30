from django.contrib import admin
from crowdFunding.models import Category, Tag, myUser

# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(myUser)