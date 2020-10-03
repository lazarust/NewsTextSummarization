from django.db import models


class User(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=25, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
