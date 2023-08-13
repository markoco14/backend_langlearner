from rest_framework.response import Response
from rest_framework.decorators import api_view

from post.models import PostContent
from ..utils import reader_utils

@api_view(['GET'])
def get_post_content_with_pinyin(request, post_pk, level_pk):
    try:
        post_content = PostContent.objects.get(post_id=post_pk, level=level_pk)
        data = {
            "id": post_content.post.id,
            "content": reader_utils.convert_to_chinese_with_pinyin(post_content.content),
            "title": post_content.post.title
        }

        return Response(data)

    except:
        return Response({})