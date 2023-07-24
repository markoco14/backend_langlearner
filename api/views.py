from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.serializers import PostContentSerializer, PostSerializer
from posts.models import Post

# Create your views here.
@api_view(['GET'])
def helloWorld(request):
    return Response({"message": "Hello World"})

@api_view(['GET'])
def get_posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def write_post(request):
    serializer = PostSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response("something went wrong")
    
@api_view(['POST'])
def write_post_content(request):
    serializer = PostContentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response("something went wrong")
    
