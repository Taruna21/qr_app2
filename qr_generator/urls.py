from django.urls import path
from . import views

urlpatterns = [
    path('input_url/', views.input_url, name='input_url'),
]
