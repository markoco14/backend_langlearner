from django.contrib import admin

from post.models import Post, PostContent, PostContentAudio, PostContentPinyin

# Register your models here.
admin.site.register(Post)
admin.site.register(PostContent)
admin.site.register(PostContentPinyin)
admin.site.register(PostContentAudio)