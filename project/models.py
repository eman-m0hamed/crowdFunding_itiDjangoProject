from django.db import models
from django.utils.text import slugify
from PIL import Image
from user.models import myUser
from django.core.validators import MinValueValidator, MaxValueValidator

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
    created_at = models.DateTimeField(auto_now_add=True)
    donation=models.IntegerField(default=0)
    averageRate = models.IntegerField(default=0)
    is_selected_by_admin = models.BooleanField(default=0)

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
    project = models.ForeignKey(Project, related_name='project_pictures', on_delete=models.CASCADE)


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


class ProjectReport(models.Model):
    reason = models.TextField()
    user = models.ForeignKey(myUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.user.first_name} {self.user.last_name} reports {self.project.title} project "

class CommentReport(models.Model):
    reason = models.TextField()
    user = models.ForeignKey(myUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} reports id = {self.comment.id} comment"

class ProjectRate(models.Model):
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(myUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} rate id = {self.comment.id} project with rate {self.rate}"

