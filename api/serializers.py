from rest_framework import serializers

from posts.models import Post, PostContent, PostContentAudio, PostContentPinyin


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostContent
        fields = '__all__'

class PostContentAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostContentAudio
        fields = '__all__'


class PostContentPinyinSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostContentPinyin
        fields = '__all__'


class ReadPostSerializer(serializers.Serializer):
    class Meta:
        fields = 'id, content, title'
