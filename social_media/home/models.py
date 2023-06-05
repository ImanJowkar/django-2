from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    
    def __str__(self):
        return f'{self.slug}'
    
    
    
    def get_absolute_url(self):
        return reverse("home:post-detail", args=(self.id, self.slug))
    