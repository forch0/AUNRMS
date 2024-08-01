from django.urls import path
from .views import generate_rooms, index

urlpatterns = [
    path('', index, name='index'),
    path('admin/dorms/dorm/generate-rooms/', generate_rooms, name='dorm_generate_rooms'),
]
