from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.serializers import ContentAudioSerializer, PostContentSerializer, ContentWithAudioSerializer
from post.models import PostContent, ContentAudio
import jieba


@api_view(['GET'])
def get_post_content(request, post_pk):
    try:
        post_content = PostContent.objects.get(post_id=post_pk)
        serializer = PostContentSerializer(post_content, many=False)

        return Response(serializer.data)

    except:
        return Response({})


@api_view(['GET'])
def get_post_content_by_id_level(request, post_pk, level_pk):
    try:
        post_content = PostContent.objects.get(post__id=post_pk, level=level_pk)
        serializer = ContentWithAudioSerializer(post_content, many=False)

        return Response(serializer.data)
    
    except PostContent.DoesNotExist:
        return Response('content does not exist')
    
    except Exception as e:
        return Response({'error': str(e)})


@api_view(['POST'])
def write_post_content(request, post_pk):
    content = request.data['content']
    chinese_segments: [] = []
    for section in content:
        if type(section).__name__ == 'list':
            list_segment: [] = []
            for item in section:
                list_segment.append(jieba.lcut(item, cut_all=False))
            chinese_segments.append(list_segment)
        else:
            chinese_segments.append(jieba.lcut(section, cut_all=False))

    request_data = {
        'post': post_pk,
        'content': chinese_segments,
        'level': request.data['level']
    }
    serializer = PostContentSerializer(data=request_data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response("something went wrong")


@api_view(['PUT'])
def update_post_content(request, pk):
    post_content = PostContent.objects.get(id=pk)
    content = request.data['content']
    chinese_segments: [] = []
    for section in content:
        if type(section).__name__ == 'list':
            list_segment: [] = []
            for item in section:
                list_segment.append(jieba.lcut(item, cut_all=False))
            chinese_segments.append(list_segment)
        else:
            chinese_segments.append(jieba.lcut(section, cut_all=False))

    # HERE WE HAVE CHINESE SEGMENTS BUT NO PINYIN
    for segment in chinese_segments:
        if type(segment[0]).__name__ == 'list':
            for item in segment:
                print(item)
        else:
            print(type(segment))
            print(segment)

    request_data = {
        'content': chinese_segments
    }
    serializer = PostContentSerializer(
        instance=post_content, data=request_data, partial=True)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def delete_post_content(request, pk):
    post_content = PostContent.objects.get(id=pk)
    post_content.delete()

    return Response("Post content gone!")

@api_view(['GET'])
def get_post_content_audio(request, pk):
    post_content_audio = ContentAudio.objects.get(post_content__id=pk)
    serializer = ContentAudioSerializer(post_content_audio)

    return Response(serializer.data)

