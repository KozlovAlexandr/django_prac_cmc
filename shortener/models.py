import random
import string

from django.conf import settings
from django.db import models


def get_brief_url():

    return ''.join(random.choices(string.ascii_letters + string.digits, k=5))


class ShortUrl(models.Model):

    hash = models.CharField(max_length=30, default=get_brief_url)
    originalUrl = models.URLField(null=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(null=True)
    clicked = models.PositiveIntegerField(default=0)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['creation_date']),
            models.Index(fields=['expiration_date']),
        ]
