from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.title


class PostContent(models.Model):
    post = models.ForeignKey(
        Post, related_name='content', on_delete=models.CASCADE)
    content = models.TextField()
    level = models.IntegerField(default=0)

    def __str__(self):
        return f"Content for {self.post.title}"
    
    class Meta:
        db_table='posts_post_content'
        verbose_name_plural='Post content'
        unique_together=['post', 'level']
        


class PostContentPinyin(models.Model):
    pinyin_content = models.TextField()
    post_content = models.OneToOneField(
        PostContent, related_name='pinyin', on_delete=models.CASCADE)

    def __str__(self):
        return f"Pinyin for {self.post_content.post.title}"
    
    class Meta:
        db_table='posts_post_content_pinyin'
        verbose_name_plural='Post content pinyin'
