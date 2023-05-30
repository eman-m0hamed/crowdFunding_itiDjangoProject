from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.text import slugify
from PIL import Image
from django.core.validators import RegexValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class myUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile_phone = models.CharField(max_length=11)
    profile_picture = models.ImageField(upload_to='profile_pictures')
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile_phone', 'email']

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)
    def _str_(self):
            return self.name
    

 
class Project(models.Model):
    user = models.ForeignKey(myUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    details = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.PROTECT, default=1)
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    pictures = models.ManyToManyField('ProjectPicture', blank=True,related_name='project_pictures')
    tags = models.ManyToManyField('Tag', blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title


class ProjectPicture(models.Model):
    image = models.ImageField(upload_to='project_pictures')
    project = models.ForeignKey(
        'Project',
        related_name='project_pictures',
        on_delete=models.CASCADE
    )


   

