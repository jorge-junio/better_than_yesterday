from django.conf import settings
from django.db import models


class ProfilePhoto(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile_photo')
    image = models.BinaryField()
    updated_at = models.DateTimeField(auto_now=True)
