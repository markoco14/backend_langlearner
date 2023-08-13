import time
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.serializers import PostContentAudioSerializer, PostContentPinyinSerializer, PostContentSerializer
from posts.models import PostContent, PostContentPinyin
import pinyin
import jieba
from google.cloud import texttospeech, storage
from google.cloud import texttospeech_v1beta1 as tts

# Create your views here.


@api_view(['GET'])
def helloWorld(request):
    return Response("hello world")

#
#
#
# READER VIEWS
#
#
#

def convert_to_chinese_with_pinyin(chinese_content):
    content_with_pinyin = []
    for sentence in chinese_content:
        pinyin_sentence = []
        for character in sentence:
            py = pinyin.get(character)
            pinyin_sentence.append({
                "chinese": character,
                "pinyin": ''.join([item for sublist in py for item in sublist])
            })
        content_with_pinyin.append(pinyin_sentence)
    return content_with_pinyin


@api_view(['GET'])
def get_post_content_with_pinyin(request, post_pk, level_pk):
    try:
        post_content = PostContent.objects.get(post_id=post_pk, level=level_pk)
        data = {
            "id": post_content.post.id,
            "content": convert_to_chinese_with_pinyin(post_content.content),
            "title": post_content.post.title
        }

        return Response(data)

    except:
        return Response({})

#
#
#
# LANGUAGE PROCESSING VIEWS
#
#
#
@api_view(['GET'])
def get_pinyin_content_by_post_id(request, pk):
    try:
        pinyin = PostContentPinyin.objects.filter(
            post_content__post__id=pk,
            post_content__level=0 
        ).first()
        serializer = PostContentPinyinSerializer(pinyin)

        return Response(serializer.data)
    except:

        return Response({})


@api_view(['GET'])
def create_post_pinyin(request, pk):
    post_content = PostContent.objects.get(id=pk)
    # get post content as list to iterate through
    content = post_content.content

    # I want the characters as single characters
    content_as_list = list(content)
    # convert each character into pinyin and store in pinyin list
    pinyin_content_list = []
    for char in content_as_list:
        pinyin_content_list.append({
            "pinyin": pinyin.get(char),
            "chinese": char
        })
    # join into pinyin string so characters can be matched on frontend
    pinyin_string = ' '.join(item['pinyin'] for item in pinyin_content_list)
    
    # pair the data for the serializer
    data={
        "pinyin_content": pinyin_string,
        "post_content": pk
    }
    serializer = PostContentPinyinSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response({})




@api_view(['GET'])
def create_segments(request, pk):
    post_content = PostContent.objects.get(id=pk)
    content = post_content.content
    word_segments = jieba.lcut(content, cut_all=False)

    return Response(word_segments)



# what are the steps
# 1) choose a title for the article (can change later)
# 2) make the article content
# 3) get the voice
# 4) set up storage
# 5) get the pinyin
# 6) get the segments
# 7) get the timestamps (update voice)
# 8) get the dictionary (because you can make copy/paste/translate easily for now)
