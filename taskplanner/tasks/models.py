from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()  # Add this line
    time = models.TimeField(default="09:00:00")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

from django.db import models

class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class BackgroundImage(models.Model):
    label = models.ForeignKey(Label, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='background_images/')
    
    def __str__(self):
        return f'{self.label.name} - {self.id}'
