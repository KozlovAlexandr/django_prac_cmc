from django.db import models

from django.contrib.auth.models import User

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.CharField(max_length=2048)
    about = models.CharField(max_length=256)
    avatarPath = models.CharField(max_length=4096)
    
    
    

# Create your models here.
