import random
import string

from django.conf import settings
from django.db import models
from datetime import datetime


def get_brief_url():

    while True:

        candidate = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        if not ShortUrl.objects.filter(hash=candidate):
            return candidate


class UnexpiredUrlManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(expiration_date__gt=datetime.now())


class ExpiredUrlManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(expiration_date__lte=datetime.now())


class ShortUrl(models.Model):

    hash = models.CharField(max_length=30, default=get_brief_url)
    original_url = models.URLField(verbose_name="Original url", null=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(null=True)
    clicked = models.PositiveIntegerField(default=0)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    objects = models.Manager()
    unexpired_objects = UnexpiredUrlManager()
    expired_objects = ExpiredUrlManager()

    class Meta:
        indexes = [
            models.Index(fields=['creation_date']),
            models.Index(fields=['expiration_date']),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(creation_date__lt=models.F('expiration_date'))
                                   , name='shortener_created_lt_expired'),
        ]
