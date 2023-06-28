from django.db import models
from django.utils import timezone


class Users(models.Model):
    name = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
