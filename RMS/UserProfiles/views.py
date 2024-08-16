from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.http import HttpResponse
from .forms import *

def index(request):
    return HttpResponse("Welcome to AUN ResLife App.")

class StaffLoginView(LoginView):
    template_name = 'userprofiles/staff_login.html'
    form_class = StaffLoginForm
    success_url = reverse_lazy('staff_dashboard')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, email=email, password=password)
        if user is not None and user.is_staff:
            login(self.request, user)
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)
        

class ResidentLoginView(LoginView):
    template_name = 'userprofiles/resident_login.html'
    form_class = ResidentLoginForm
    success_url = reverse_lazy('resident_dashboard')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        room_number = form.cleaned_data['room_number']
        password = form.cleaned_data['password']
        user = authenticate(self.request, email=email, room_number=room_number, password=password)
        if user is not None and not user.is_staff:
            login(self.request, user)
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)
        
@login_required
def staff_dashboard(request):
    return render(request, 'userprofiles/staff_dashboard.html')

@login_required
def resident_dashboard(request):
    return render(request, 'userprofiles/resident_dashboard.html')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Redirect to login page after logout