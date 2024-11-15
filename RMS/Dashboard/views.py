from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.http import HttpResponse
from AcademicYear.models import Semester
from django.utils import timezone

def index(request):
    return HttpResponse("Welcome to Dashboard Section.")


# from django.shortcuts import render
# from .models import Semester

# def admin_dashboard(request):
#     current_semester = Semester.objects.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now()).first()
    
#     return render(request, 'admin/index.html', {'current_semester': current_semester})
