from django.db import models

# Create your models here.

class Post(models.Model):
    title=models.CharField(max_length=100, default="")
    
class PostContent(models.Model):
    content=models.TextField()
    level=models.CharField(max_length=50, default="")
    post=models.ForeignKey(Post, related_name='posts_content', on_delete=models.CASCADE)
    class Meta:
        unique_together=['level', 'post']