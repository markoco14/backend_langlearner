from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.serializers import PostSerializer
from posts.models import Post

# Create your views here.
@api_view(['GET'])
def helloWorld(request):
    return Response({"message": "Hello World"})

@api_view(['POST'])
def write_post(request):
    serializer = PostSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response("something went wrong")
    
