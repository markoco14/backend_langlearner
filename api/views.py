import time
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.serializers import PostContentSerializer, PostSerializer
from posts.models import Post, PostContent
import pinyin
import jieba
from google.cloud import texttospeech, storage

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
def write_post_content(request, post_pk):
    request_data = {
        'post': post_pk,
        'content': request.data['content']
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


def upload_blob_from_memory(bucket_name, contents, destination_blob_name):
    """Uploads a file to the bucket."""

    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The contents to upload to the file
    # contents = "these are my contents"

    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(contents)
    blob.make_public()
    public_url = blob.public_url

    print(
        f"{destination_blob_name} with contents {contents} uploaded to {bucket_name} with public url {public_url}."
    )

    return public_url


@api_view(['GET'])
def get_tts(request, pk):
    post_content = PostContent.objects.get(id=pk)
    content = post_content.content

    tts_client = texttospeech.TextToSpeechClient()
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
    response = tts_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    # UPLOAD FILE TO STORAGE
    bucket_name = 'twle-445f4.appspot.com'
    contents = response.audio_content
    destination_blob_name = "chinese/" + \
        str(round(time.time() * 1000)) + ".mp3"

    public_url = upload_blob_from_memory(
        bucket_name, contents, destination_blob_name)

    # REPLACE WITH CLOUD STORAGE
    # with open("./files/male.mp3", "wb") as out:
    #     # Write the response to the output file.
    #     out.write(response.audio_content)

    return Response({
        'message': 'Audio content saved to cloud storage',
        'public-url': public_url
    })


@api_view(['GET'])
def get_audio_url(request):
    # FOR NOW I WILL STORE THE URL IN A TABLE
    # AND IT WILL BE A PUBLIC URL
    bucket_name = 'twle-445f4.appspot.com'
    blob_name = 'chinese/1690267027531.mp3'
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # FOR LATER I WILL SET UP THE PERMISSIONS
    # TO LET ME MAKE A TEMPORARY SIGNED URL
    # THAT WILL LET ME STORE THE URL ON THE USER'S DEVICE
    # AND ONLY HAVE TO RE-REQUEST WHEN THOSE URLS ARE EXPIRED
    # Make the blob publicly accessible for a duration.
    # Note: In this case the duration is 1 hour (3600 seconds).
    # url = blob.generate_signed_url(
    #     # This URL will be valid for 1 hour
    #     expiration=datetime.timedelta(seconds=3600),
    #     # Allow GET requests using this URL.
    #     method='GET'
    # )

    return Response({
        "url": "https://storage.googleapis.com/twle-445f4.appspot.com/chinese/1691211111218.mp3"
    })
    # return file


# what are the steps
# 1) choose a title for the article (can change later)
# 2) make the article content
# 3) get the voice
# 4) set up storage
# 5) get the pinyin
# 6) get the segments
# 7) get the timestamps (update voice)
# 8) get the dictionary (because you can make copy/paste/translate easily for now)
