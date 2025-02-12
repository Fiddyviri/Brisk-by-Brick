from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length= 150)
    last_name = models.CharField(max_length= 150)
    username =models.CharField(unique=True, max_length= 150)
    bio = models.TextField(blank=True, null=True)
    profile_img = models.ImageField(upload_to='profile/', null=True, blank=True)
    
    def _str_(self):
        return self.username