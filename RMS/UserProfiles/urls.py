from django.urls import path
from . import views
from .views import StaffRegistrationView, ResidentRegistrationView, StaffDashboardView, ResidentDashboardView

urlpatterns = [
    path('', views.index, name='index'),
    path('staff/register/', StaffRegistrationView.as_view(), name='staff_register'),
    path('resident/register/', ResidentRegistrationView.as_view(), name='resident_register'),
    path('staff/dashboard/', StaffDashboardView.as_view(), name='staff_dashboard'),
    path('resident/dashboard/', ResidentDashboardView.as_view(), name='resident_dashboard'),
    # ... other paths

#     # Add other paths as needed
]
