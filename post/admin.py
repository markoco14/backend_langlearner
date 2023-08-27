from django.contrib import admin

from post.models import Post, PostContent, ContentAudio, ContentPinyin

# Register your models here.
admin.site.register(Post)
admin.site.register(PostContent)
admin.site.register(ContentPinyin)
admin.site.register(ContentAudio)