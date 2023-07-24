from rest_framework import serializers

from posts.models import Post, PostContent

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields='__all__'
        
class PostContentSerializer(serializers.ModelSerializer):
		class Meta:
				model=PostContent
				fields='__all__'