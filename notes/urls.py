from django.urls import path
from . import views

urlpatterns = [
    path('create_note', views.create_note, name='create_note')
]