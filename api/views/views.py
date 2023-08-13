import time
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.serializers import PostContentAudioSerializer, PostContentPinyinSerializer, PostContentSerializer
from posts.models import PostContent, PostContentPinyin
import pinyin
import jieba
from google.cloud import texttospeech, storage
from google.cloud import texttospeech_v1beta1 as tts

# Create your views here.


@api_view(['GET'])
def helloWorld(request):
    return Response("hello world")

#
#
#
# READER VIEWS
#
#
#

def convert_to_chinese_with_pinyin(chinese_content):
    content_with_pinyin = []
    for sentence in chinese_content:
        pinyin_sentence = []
        for character in sentence:
            py = pinyin.get(character)
            pinyin_sentence.append({
                "chinese": character,
                "pinyin": ''.join([item for sublist in py for item in sublist])
            })
        content_with_pinyin.append(pinyin_sentence)
    return content_with_pinyin


@api_view(['GET'])
def get_post_content_with_pinyin(request, post_pk, level_pk):
    try:
        post_content = PostContent.objects.get(post_id=post_pk, level=level_pk)
        data = {
            "id": post_content.post.id,
            "content": convert_to_chinese_with_pinyin(post_content.content),
            "title": post_content.post.title
        }

        return Response(data)

    except:
        return Response({})


#
#
#
# POST CONTENT VIEWS
#
#
#

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
        post_content = PostContent.objects.get(post_id=post_pk, level=level_pk)
        serializer = PostContentSerializer(post_content, many=False)

        return Response(serializer.data)

    except:
        return Response({})


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

    # HERE WE HAVE CHINESE SEGMENTS BUT NO PINYIN
    for segment in chinese_segments:
        if type(segment[0]).__name__ == 'list':
            for item in segment:
                print(item)
        else:
            print(type(segment))
            print(segment)

    print(type(chinese_segments))
    # return Response({})
        # if type(section).__name__ == 'list':
        #     for item in segment:
        #         print(item)
        # else:
        #     print(segment)
    # return Response({})
    # paragraphs = [p.strip() for p in content.split("\n\n") if p.strip() != ""]
    # print(paragraphs)
    # print(content)
    # content_as_list = list(content)
    # print(content_as_list)
    # word_segments = jieba.lcut(content, cut_all=False)
    # print(word_segments)

    # pinyin_content_list = []
    # for segment in word_segments:
    #     # pinyin_segment = pinyin.get(segment)
    #     pinyin_translation = ''.join(pinyin.get(segment))
    #     pinyin_content_list.append(pinyin_translation)
    
    # print(pinyin_content_list)

    # print('length of chinese segments', len(word_segments))
    # print('length of pinyin segments', len(pinyin_content_list))
    # return Response({})
    # print(json.dumps(chinese_segments))
    # return Response({})
    request_data = {
        'post': post_pk,
        'content': chinese_segments
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


def concatenate_characters(array):
    return ''.join(''.join(subarray) for subarray in array)

@api_view(['GET'])
def create_tts(request, pk):
    post_content = PostContent.objects.get(id=pk)
    
    content_as_string = concatenate_characters(post_content.content)

    tts_client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=content_as_string)
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
    
    
    data = {
        "post_content": post_content.id,
        "audio_url": public_url,
        "timestamps": 'timestamps'
    }

    serializer = PostContentAudioSerializer(data=data)
    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data)


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
