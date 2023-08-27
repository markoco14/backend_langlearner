from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.pagination import PageNumberPagination

from cedict.models import Word
from cedict.serializers import WordSerializer

@api_view(['GET'])
def listWords(request):	
    words = Word.objects.all()
    paginator = PageNumberPagination()
    paginated_queryset = paginator.paginate_queryset(words, request)
    serializer = WordSerializer(paginated_queryset, many=True)
    return paginator.get_paginated_response(serializer.data)