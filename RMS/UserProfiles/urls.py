from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Example view
    # Add more paths as needed
]