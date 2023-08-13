from django.db import models

from users.models import User

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100, default="")
    user = models.ForeignKey(User, default=1, related_name='user', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} (id: {self.id})"
    
    class Meta:
        unique_together=['title', 'user']


class PostContent(models.Model):
    post = models.ForeignKey(
        Post, related_name='content', on_delete=models.CASCADE)
    content = models.JSONField()
    level = models.IntegerField(default=0)

    def __str__(self):
        return f"Content for {self.post.title} (level: {self.level})"
    
    class Meta:
        db_table='post_post_content'
        verbose_name_plural='Post content'
        unique_together=['post', 'level']


class PostContentAudio(models.Model):
    post_content = models.ForeignKey(PostContent, related_name='audio', on_delete=models.CASCADE)
    audio_url = models.CharField(max_length=255)
    timestamps = models.JSONField()

    def __str__(self):
        return f"Audio data for {self.post_content.post.title} (level: {self.post_content.level})"
    
    class Meta:
        db_table='post_post_content_audio'
        verbose_name_plural='Post content audio'
        unique_together=['post_content', 'audio_url']


class PostContentPinyin(models.Model):
    pinyin_content = models.TextField()
    post_content = models.OneToOneField(
        PostContent, related_name='pinyin', on_delete=models.CASCADE)

    def __str__(self):
        return f"Pinyin for {self.post_content.post.title} (level: {self.post_content.level})"
    
    class Meta:
        db_table='post_post_content_pinyin'
        verbose_name_plural='Post content pinyin'
