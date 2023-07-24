from django.urls import path
from . import views

urlpatterns = [
    # GREETING ROUTE
    path('', views.helloWorld, name='hello-world'),


    path('write-post/', views.write_post, name='write-post'),
]