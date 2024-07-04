from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to AUN ResLife App.")
class StaffLoginView(LoginView):
    template_name = 'staff_login.html'
    success_url = reverse_lazy('staff_dashboard')

class ResidentLoginView(LoginView):
    template_name = 'resident_login.html'
    success_url = reverse_lazy('resident_dashboard')

@login_required
def staff_dashboard(request):
    return render(request, 'staff_dashboard.html')

@login_required
def resident_dashboard(request):
    return render(request, 'resident_dashboard.html')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Redirect to login page after logout
