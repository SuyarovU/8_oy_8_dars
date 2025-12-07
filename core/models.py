from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    title = models.CharField()
    description = models.TextField()
    completed = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
