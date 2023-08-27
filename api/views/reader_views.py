from rest_framework.response import Response
from rest_framework.decorators import api_view

from post.models import ContentAudio, PostContent
from ..utils import reader_utils

@api_view(['GET'])
def get_post_for_reader(request, post_pk, level_pk):
    try:
        post_content = PostContent.objects.get(post_id=post_pk, level=level_pk)
        post_audio = ContentAudio.objects.get(post_content=post_content.id)
        data = {
            "id": post_content.post.id,
            "content": reader_utils.convert_to_chinese_with_pinyin(post_content.content),
            "title": post_content.post.title,
            "audio_url": post_audio.audio_url
        }

        return Response(data)

    except:
        return Response({})