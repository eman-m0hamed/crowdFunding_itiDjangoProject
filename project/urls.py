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

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.ProjectsView.as_view(), name='projects'),
    path('<int:id>/', views.ProjectDetails.as_view(), name='ProjectDetails'),
    path('<int:id>/Donations/', views.DonationsView.as_view(), name='donations'),
    path('<int:id>/comments/', views.ProjectComments.as_view(), name='project-comments'),
    path('lastFiveProjects/', views.LastFiveProjects.as_view(), name='last-five-projects'),
    path('<int:id>/reports/', views.ReportProject.as_view(), name='project-report'),
    path('<int:projectId>/comments/<int:id>/reports/', views.ReportComment.as_view(), name='comment-report'),
    path('<int:id>/rates/', views.RateProject.as_view(), name='project-rate'),
    path('HighestFiveRated/', views.HighestFiveRated.as_view(), name='highest-five-rated-projects'),
    path('lastFiveProjectSelectedByAdmin/', views.lastFiveProjectSelectedByAdmin.as_view(), name='highest-five-rated-projects'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






