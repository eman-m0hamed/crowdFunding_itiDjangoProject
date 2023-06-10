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
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.UserListCreateAPIView.as_view(), name='user-list'),
    path('<int:pk>/', views.UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),
   # path('users/<int:user_id>/projects/', views.UserProjectListAPIView.as_view(), name='user-project-list'),
    path('register/', views.UserView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('email-verify/', views.VarifyEmail.as_view(), name="email-verify"),
    path('verifyEmailResult/', views.verifyEmailResult, name="email-verify-result"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






