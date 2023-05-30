"""
URL configuration for crowdFunding project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from crowdFunding import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', views.UserListCreateAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),
    path('projects/', views.ProjectListCreateAPIView.as_view(), name='project-list'),
    path('projects/<int:pk>/', views.ProjectRetrieveUpdateDestroyAPIView.as_view(), name='project-detail'),
    path('categories/', views.CategoryListCreateAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail'),
    path('project-pictures/', views.ProjectPictureListCreateAPIView.as_view(), name='project-picture-list'),
    path('project-pictures/<int:pk>/', views.ProjectPictureRetrieveUpdateDestroyAPIView.as_view(), name='project-picture-detail'),
    path('tags/', views.TagListCreateAPIView.as_view(), name='tag-list'),
    path('tags/<int:pk>/', views.TagRetrieveUpdateDestroyAPIView.as_view(), name='tag-detail'),
    path('users/<int:user_id>/projects/', views.UserProjectListAPIView.as_view(), name='user-project-list'),
    path('users/login/', views.UserLoginView.as_view(), name='login')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



     


