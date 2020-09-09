from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Lang(models.Model):
    
    name = models.CharField(max_length=20, blank=True)

class Paste(models.Model):
    
    url = models.CharField(max_length=4096)
    title = models.CharField(max_length=255)
    syntax = models.ForeignKey("Lang", on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True)
    expirationDate = models.DateTimeField(null=True)  
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    catalog = models.ForeignKey("pasteCatalog", on_delete=models.CASCADE, null=True)

class pasteCatalog(models.Model):
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True)


# Create your models here.
