from django.db import models
from django.conf import settings
import random
import string
from datetime import datetime


class Lang(models.Model):
    name = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.name


def get_url_hash():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


class PasteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(expiration_date__gt=datetime.now())


class Paste(models.Model):
    hash = models.CharField(max_length=4096, default=get_url_hash, blank=False)
    title = models.CharField(max_length=255, blank=False)
    syntax = models.ForeignKey("Lang", on_delete=models.CASCADE, blank=False, null=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(null=True)
    text = models.TextField(blank=False)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    catalog = models.ForeignKey("pasteCatalog", on_delete=models.CASCADE, null=True, blank=True)

    objects = models.Manager()
    unexpired_objects = PasteManager()

    def __str__(self):
        return "{}|{}".format(self.id, self.title)

    class Meta:
        indexes = [
            models.Index(fields=['creation_date']),
            models.Index(fields=['expiration_date']),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(creation_date__lt=models.F('expiration_date'))
                                   , name='created_lt_expired'),
        ]


class PasteCatalog(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return "{}|{}".format(self.owner.username, self.name)

# Create your models here.
