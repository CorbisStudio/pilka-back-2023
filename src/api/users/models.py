from django.db import models


class Users(models.Model):
    name = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    email = models.EmailField()

    # Otros campos y métodos relevantes

    def __str__(self):
        return self.name
