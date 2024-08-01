# views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RoomGenerationForm
from .models import Dorm, Room
from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to Dorms Section.")

# 