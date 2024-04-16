from django.urls import path
from saves import views

urlpatterns = [
    path('saves/', views.SaveList.as_view()),
    path('saves/<int:pk>/', views.SaveDetail.as_view())
]
