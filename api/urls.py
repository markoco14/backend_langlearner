from django.urls import path

from cedict import views as cedict_views
from .views import post_views, post_content_views, tts_views, reader_views

urlpatterns = [

    # POST CRUD ROUTES
    path('posts/', post_views.get_posts, name='get-posts'),
    path('posts/write/', post_views.create_post, name='write-post'),
    path('posts/<str:pk>/update/', post_views.update_post, name='update-post'),
    path('posts/<str:pk>/delete/', post_views.delete_post, name='delete-post'),

    # POST CONTENT CRUD ROUTES
    path('posts/<str:post_pk>/content/',
         post_content_views.get_post_content, name='get-post-content'),
    path('posts/<str:post_pk>/content/level/<str:level_pk>/',
         post_content_views.get_post_content_by_id_level, name='get-post-content-id-level'),
    path('posts/<str:post_pk>/content/write/',
         post_content_views.write_post_content, name='write-post-content'),
    path('posts/content/<str:pk>/update/',
         post_content_views.update_post_content, name='update-post-content'),
    path('posts/content/<str:pk>/delete/',
         post_content_views.delete_post_content, name='delete-post-content'),

    # POST CONTENT AUDIO CRUD ROUTES
    path('posts/content/<str:pk>/audio/',
         post_content_views.get_post_content_audio, name='get-post-content-audio'),

    # TTS ROUTES
    path('posts/content/<str:content_pk>/audio/create/',
         tts_views.create_tts, name='get-audio'),

    # READER ROUTES
    path('read/posts/<str:post_pk>/level/<str:level_pk>/',
         reader_views.get_post_for_reader, name='post-for-reader'),

    path('words/', cedict_views.listWords, name='list-words'),
    path('words/<str:word_pk>/', cedict_views.getWord, name='get-word'),
]
