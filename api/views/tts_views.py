import time
from rest_framework.response import Response
from rest_framework.decorators import api_view

from ..utils import tts_utils
from api.serializers import PostContentAudioSerializer
from posts.models import PostContent
from google.cloud import texttospeech
from google.cloud import texttospeech_v1beta1 as tts_v1


@api_view(['GET'])
def create_tts(request, pk):
    post_content = PostContent.objects.get(id=pk)
    
    content_as_string = tts_utils.concatenate_characters(post_content.content)

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

    public_url = tts_utils.upload_blob_from_memory(
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

#
# 
# SAVE FOR LATER WHEN WE USE CREDENTIALS
# TO MAKE TEMPORARY SIGNED URLS
# 
#  

# @api_view(['GET'])
# def get_audio_url(request):
#     # FOR NOW I WILL STORE THE URL IN A TABLE
#     # AND IT WILL BE A PUBLIC URL
#     bucket_name = 'twle-445f4.appspot.com'
#     blob_name = 'chinese/1690267027531.mp3'
#     storage_client = storage.Client()
#     bucket = storage_client.get_bucket(bucket_name)
#     blob = bucket.blob(blob_name)

#     # FOR LATER I WILL SET UP THE PERMISSIONS
#     # TO LET ME MAKE A TEMPORARY SIGNED URL
#     # THAT WILL LET ME STORE THE URL ON THE USER'S DEVICE
#     # AND ONLY HAVE TO RE-REQUEST WHEN THOSE URLS ARE EXPIRED
#     # Make the blob publicly accessible for a duration.
#     # Note: In this case the duration is 1 hour (3600 seconds).
#     # url = blob.generate_signed_url(
#     #     # This URL will be valid for 1 hour
#     #     expiration=datetime.timedelta(seconds=3600),
#     #     # Allow GET requests using this URL.
#     #     method='GET'
#     # )

#     return Response({
#         "url": "https://storage.googleapis.com/twle-445f4.appspot.com/chinese/1691211111218.mp3"
#     })
#     # return file