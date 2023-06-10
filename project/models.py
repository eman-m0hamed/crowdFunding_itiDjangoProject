from django.db import models
from django.utils.text import slugify
from PIL import Image
from user.models import myUser
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Project(models.Model):
    user = models.ForeignKey(myUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    total_target = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50)
    project = models.ForeignKey(
        Project,
        related_name='project_tages',
        on_delete=models.CASCADE
    )
    def _str_(self):
            return self.name


class ProjectPicture(models.Model):
    image = models.ImageField(upload_to='project_pictures')
    project = models.ForeignKey(
        Project,
        related_name='project_pictures',
        on_delete=models.CASCADE
    )

class Comments(models.Model):
    comment = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(myUser, on_delete=models.CASCADE)

    def __str__(self):
        return (f"{self.user.first_name} {self.user.last_name} on {self.project.title}")


class Donations(models.Model):
    money = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(myUser, on_delete=models.CASCADE)

    def __str__(self):
        return (f"{self.user} Donate to {self.project}")

