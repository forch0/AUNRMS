from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
#     path('staff/login/', views.StaffLoginView.as_view(), name='staff_login'),
#     path('resident/login/', views.ResidentLoginView.as_view(), name='resident_login'),
#     path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
#     path('resident/dashboard/', views.resident_dashboard, name='resident_dashboard'),
#     path('logout/', views.CustomLogoutView.as_view(), name='logout'),
#     # Add other paths as needed
]
