from django.urls import path
from . import views

urlpatterns = [
    # GREETING ROUTE
    path('', views.helloWorld, name='hello-world'),

    path('posts/', views.get_posts, name='get-posts'),
    path('posts/write/', views.write_post, name='write-post'),

    path('posts/content/write/', views.write_post_content, name='write-post-content')
]