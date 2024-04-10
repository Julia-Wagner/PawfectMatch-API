from django.urls import path
from dogs import views

urlpatterns = [
    path('dogs/', views.DogList.as_view()),
    path('dogs/<int:pk>/', views.DogDetail.as_view()),
]
