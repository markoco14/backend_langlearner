from django.urls import path
from . import views

urlpatterns = [
    # GREETING ROUTE
    path('', views.helloWorld, name='hello-world'),

    path('posts/', views.get_posts, name='get-posts'),
    path('posts/write/', views.write_post, name='write-post'),
    path('posts/update/<str:pk>/', views.update_post, name='update-post'),
    path('posts/delete/<str:pk>/', views.delete_post, name='delete-post'),

    path('posts/content/', views.get_post_contents, name='get-post-contents'),
    path('posts/content/write/', views.write_post_content, name='write-post-content'),
    path('posts/content/update/<str:pk>/', views.update_post_content, name='update-post-content'),
    path('posts/content/delete/<str:pk>/', views.delete_post_content, name='delete-post-content'),

    path('posts/content/<str:pk>/pinyin/', views.get_post_pinyin, name='get-post-pinyin'),
    path('posts/content/<str:pk>/segments/', views.get_segments, name='get-segments'),
    path('posts/content/<str:pk>/audio/', views.get_tts, name='get-audio'),

]