from django.contrib import admin

from posts.models import Post, PostContent

# Register your models here.
admin.site.register(Post)
admin.site.register(PostContent)