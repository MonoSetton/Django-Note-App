from django.urls import path
from . import views

urlpatterns = [
    path('create_note/', views.create_note, name='create_note'),
    path('update_note/<str:pk>/', views.update_note, name='update_note'),
    path('delete_note/<str:pk>/', views.delete_note, name='delete_note'),
]