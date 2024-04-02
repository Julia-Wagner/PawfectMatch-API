from django.urls import path
from medias import views

urlpatterns = [
    path('medias/post/<int:post_id>/', views.PostMediaList.as_view()),
    path('medias/dog/<int:dog_id>/', views.DogMediaList.as_view()),
    path('medias/<int:pk>/', views.MediaDetail.as_view())
]
