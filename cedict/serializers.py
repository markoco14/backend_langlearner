from rest_framework import serializers

from cedict.models import Word



class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'
