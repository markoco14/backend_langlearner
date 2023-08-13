from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.serializers import PostContentPinyinSerializer
from posts.models import PostContent, PostContentPinyin
import pinyin
import jieba

# Create your views here.


@api_view(['GET'])
def helloWorld(request):
    return Response("hello world")

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
