from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.serializers import PostContentSerializer, PostSerializer
from posts.models import Post, PostContent
import pinyin
import jieba
from google.cloud import texttospeech

# Create your views here.


@api_view(['GET'])
def helloWorld(request):
    return Response("hello world")

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


@api_view(['PUT'])
def update_post(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(instance=post, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()

    return Response("Post gone!")

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
    serializer = PostContentSerializer(
        instance=post_content, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def delete_post_content(request, pk):
    post_content = PostContent.objects.get(id=pk)
    post_content.delete()

    return Response("Post content gone!")

#
#
#
# LANGUAGE PROCESSING VIEWS
#
#
#


@api_view(['GET'])
def get_post_pinyin(request, pk):
    post_content = PostContent.objects.get(id=pk)
    content = post_content.content
    list_content = list(content)
    pinyin_content = []
    for char in list_content:
        pinyin_content.append({
            "pinyin": pinyin.get(char),
            "chinese": char
        })

    return Response(pinyin_content)

@api_view(['GET'])
def get_segments(request, pk):
    post_content = PostContent.objects.get(id=pk)
    content = post_content.content
    word_segments = jieba.lcut(content, cut_all=False)

    return Response(word_segments)

@api_view(['GET'])
def get_tts(request, pk):
    post_content = PostContent.objects.get(id=pk)
    content = post_content.content

    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=content)
    # MALE VOICE
    voice = texttospeech.VoiceSelectionParams(
        language_code="cmn-TW",
        name="cmn-TW-Wavenet-B",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )
    # FEMAIL VOICE
    # voice = texttospeech.VoiceSelectionParams(
    #     language_code="cmn-TW",
    #     name="cmn-TW-Wavenet-A",
    #     ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    # )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    # REPLACE WITH CLOUD STORAGE
    with open("./files/male.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)

    return Response('Audio content written to ./files as "male.mp3"')


# what are the steps
# 1) choose a title for the article (can change later)
# 2) make the article content
# 3) get the voice
# 4) set up storage
# 5) get the pinyin
# 6) get the segments
# 7) get the timestamps (update voice)
# 8) get the dictionary (because you can make copy/paste/translate easily for now)