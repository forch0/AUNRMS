from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/analytics-dashboard/', analytics_dashboard, name='analytics_dashboard'),
    path('analytics/total_enrollment_by_dorm/', views.total_enrollment_by_dorm_view, name='total_enrollment_by_dorm'),
    path('analytics/enrollment_trends/', views.enrollment_trends_view, name='enrollment_trends'),
    path('analytics/resident_room_occupancy/', views.resident_room_occupancy_view, name='resident_room_occupancy'),
    path('analytics/maintenance_requests_by_category/', views.maintenance_requests_by_category_view, name='maintenance_requests_by_category'),
    path('analytics/request_completion_rate/', views.request_completion_rate_view, name='request_completion_rate'),
    path('analytics/complaint_status_analysis/', views.complaint_status_analysis_view, name='complaint_status_analysis'),
    path('analytics/anonymous_vs_non_anonymous_complaints/', views.anonymous_vs_non_anonymous_complaints_view, name='anonymous_vs_non_anonymous_complaints'),
    path('analytics/complaint_trends/', views.complaint_trends_view, name='complaint_trends'),
    path('analytics/staff_assignment_by_role/', views.staff_assignment_by_role_view, name='staff_assignment_by_role'),
    path('analytics/semester_based_dorm_usage/', views.semester_based_dorm_usage_view, name='semester_based_dorm_usage'),
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
