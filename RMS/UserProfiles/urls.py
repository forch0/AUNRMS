from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
#     path('usercreds/', UserCredListView.as_view(), name='usercred_list'),
#     path('usercreds/<uuid:pk>/', UserCredDetailView.as_view(), name='usercred_detail'),
#     path('usercreds/create/', UserCredCreateView.as_view(), name='usercred_create'),
#     path('usercreds/<uuid:pk>/update/', UserCredUpdateView.as_view(), name='usercred_update'),
#     path('usercreds/<uuid:pk>/delete/', UserCredDeleteView.as_view(), name='usercred_delete'),

#     # Residents URLs
#     path('residents/', ResidentsListView.as_view(), name='residents_list'),
#     path('residents/<uuid:pk>/', ResidentsDetailView.as_view(), name='residents_detail'),
#     path('residents/create/', ResidentsCreateView.as_view(), name='residents_create'),
#     path('residents/<uuid:pk>/update/', ResidentsUpdateView.as_view(), name='residents_update'),
#     path('residents/<uuid:pk>/delete/', ResidentsDeleteView.as_view(), name='residents_delete'),

#     # Roles URLs
#     path('roles/', RolesListView.as_view(), name='roles_list'),
#     path('roles/<uuid:pk>/', RolesDetailView.as_view(), name='roles_detail'),
#     path('roles/create/', RolesCreateView.as_view(), name='roles_create'),
#     path('roles/<uuid:pk>/update/', RolesUpdateView.as_view(), name='roles_update'),
#     path('roles/<uuid:pk>/delete/', RolesDeleteView.as_view(), name='roles_delete'),

#     # Staffs URLs
#     path('staffs/', StaffsListView.as_view(), name='staffs_list'),
#     path('staffs/<uuid:pk>/', StaffsDetailView.as_view(), name='staffs_detail'),
#     path('staffs/create/', StaffsCreateView.as_view(), name='staffs_create'),
#     path('staffs/<uuid:pk>/update/', StaffsUpdateView.as_view(), name='staffs_update'),
#     path('staffs/<uuid:pk>/delete/', StaffsDeleteView.as_view(), name='staffs_delete'),

#     # Authentication URLs
#     path('staff/register/', StaffRegistrationView.as_view(), name='staff_register'),
#     path('staff/login/', StaffLoginView.as_view(), name='staff_login'),
#     path('resident/register/', ResidentRegistrationView.as_view(), name='resident_register'),
#     path('resident/login/', ResidentLoginView.as_view(), name='resident_login'),

#     # Dashboards
#     path('staff/dashboard/', StaffDashboardView.as_view(), name='staff_dashboard'),
#     path('resident/dashboard/', ResidentDashboardView.as_view(), name='resident_dashboard'),

#     # Logout
#     path('logout/', LogoutView.as_view(), name='logout'),
# #     # Add other paths as needed
]
