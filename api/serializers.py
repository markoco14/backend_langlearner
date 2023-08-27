from rest_framework import serializers

from post.models import Post, PostContent, ContentAudio, ContentPinyin


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostContent
        fields = '__all__'

class ContentAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentAudio
        fields = '__all__'

class ContentWithAudioSerializer(serializers.ModelSerializer):
    audio = ContentAudioSerializer(read_only=True)
    
    class Meta:
        model = PostContent
        fields = ['id', 'post', 'content', 'level', 'audio']


class ContentPinyinSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentPinyin
        fields = '__all__'


class ReadPostSerializer(serializers.Serializer):
    class Meta:
        fields = 'id, content, title'
