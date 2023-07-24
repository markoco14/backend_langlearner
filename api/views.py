from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.serializers import PostContentSerializer, PostSerializer
from posts.models import Post, PostContent

# Create your views here.
@api_view(['GET'])
def helloWorld(request):
    return Response({"message": "Hello World"})

# 
# 
# 
# POST VIEWS
# 
# 
# 

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
    
# 
# 
# 
# POST CONTENT VIEWS
# 
# 
# 
    
@api_view(['GET'])
def get_post_contents(request):
    post_contents = PostContent.objects.all()
    serializer = PostContentSerializer(post_contents, many=True)

    return Response(serializer.data)

@api_view(['POST'])
def write_post_content(request):
    serializer = PostContentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response("something went wrong")
    
@api_view(['PUT'])
def update_post_content(request, pk):
    post_content = PostContent.objects.get(id=pk)
    serializer = PostContentSerializer(instance=post_content, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

    