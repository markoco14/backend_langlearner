from django.urls import path
from .views import views, post_views, post_content_views, tts_views

urlpatterns = [
    # GREETING ROUTE
    path('', views.helloWorld, name='hello-world'),

    # POST CRUD ROUTES
    path('posts/', post_views.get_posts, name='get-posts'),
    path('posts/write/', post_views.create_post, name='write-post'),
    path('posts/<str:pk>/update/', post_views.update_post, name='update-post'),
    path('posts/<str:pk>/delete/', post_views.delete_post, name='delete-post'),

    # POST CONTENT CRUD ROUTES
    path('posts/<str:post_pk>/content/', post_content_views.get_post_content, name='get-post-content'),
    path('posts/<str:post_pk>/content/level/<str:level_pk>/', post_content_views.get_post_content_by_id_level, name='get-post-content-id-level'),
    path('posts/<str:post_pk>/content/write/', post_content_views.write_post_content, name='write-post-content'),
    path('posts/content/<str:pk>/update/', post_content_views.update_post_content, name='update-post-content'),
    path('posts/content/<str:pk>/delete/', post_content_views.delete_post_content, name='delete-post-content'),

    # TTS ROUTES
    path('posts/content/<str:pk>/audio/create/', tts_views.create_tts, name='get-audio'),

    # READER ROUTES
    path('read/posts/<str:post_pk>/level/<str:level_pk>/', views.get_post_content_with_pinyin, name='content-with-pinyin'),
    
    # MISC ROUTES
    path('posts/<str:pk>/content/pinyin/', views.get_pinyin_content_by_post_id, name='get-pinyin-content'),
    path('posts/content/<str:pk>/pinyin/create/', views.create_post_pinyin, name='get-post-pinyin'),
    path('posts/content/<str:pk>/segments/create/', views.create_segments, name='get-segments'),
]