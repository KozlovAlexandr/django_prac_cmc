from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import os
from django.contrib.auth.models import User
import random, string


def get_new_image_path(instance, filename):

    ext = filename.split(".")[-1]
    candidate = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return 'images/{0}.{1}'.format(candidate, ext)


class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.CharField(max_length=2048, blank=True)
    about = models.CharField(max_length=256, blank=True)
    avatar = models.ImageField(null=True, upload_to=get_new_image_path)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()