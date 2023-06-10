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
    mobile_phone = models.CharField(max_length=11,
                    validators=[RegexValidator(r'^01[0-2,5]{1}[0-9]{8}$')])
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True)
    is_active = models.BooleanField(default=True)
    is_verifications = models.BooleanField(default=False)
    is_authenticated = models.BooleanField(null=True)
    auth_provider = models.CharField(max_length=255,blank=False,null=False,default='email')
    country = models.CharField(max_length=30, null=True, blank=True)
    Birth_date = models.DateField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile_phone', 'email']

    def __str__(self):
        return self.email


