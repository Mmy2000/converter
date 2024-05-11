from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_vtt, name='upload_vtt'),
]
