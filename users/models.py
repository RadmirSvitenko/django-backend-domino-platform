from django.contrib.auth.models import AbstractUser
from django.db import models
from favorite.models import Favorite

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=100, unique=True, verbose_name='email address')
    password = models.CharField(max_length=100, verbose_name='password')
    username = models.CharField(max_length=100, unique=True, verbose_name='username', default='', blank=True, null=True)
    avatar = models.ImageField(upload_to='media/images/user/avatar', null=True, blank=True, verbose_name='avatar-user')
    is_active = models.BooleanField(default=True, verbose_name='active')
    role = models.CharField(max_length=100, verbose_name='role', default='user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE, related_name='favorite_user', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = f"user{self.id if self.id else ''}"
        super().save(*args, **kwargs)


