from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField()
    description = models.TextField(max_length=255)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date = models.DateField()
