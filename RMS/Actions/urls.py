from django.urls import path
from . import views

from .views import *

urlpatterns = [
    path('', views.index, name='index'),

    # path('categories/', CategoryListView.as_view(), name='category_list'),
    # path('categories/<uuid:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    # path('categories/new/', CategoryCreateView.as_view(), name='category_create'),
    # path('categories/<uuid:pk>/edit/', CategoryUpdateView.as_view(), name='category_update'),
    # path('categories/<uuid:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),

    # path('subcategories/', SubCategoryListView.as_view(), name='subcategory_list'),
    # path('subcategories/<uuid:pk>/', SubCategoryDetailView.as_view(), name='subcategory_detail'),
    # path('subcategories/new/', SubCategoryCreateView.as_view(), name='subcategory_create'),
    # path('subcategories/<uuid:pk>/edit/', SubCategoryUpdateView.as_view(), name='subcategory_update'),
    # path('subcategories/<uuid:pk>/delete/', SubCategoryDeleteView.as_view(), name='subcategory_delete'),

    # path('maintenancerequests/', MaintenanceRequestListView.as_view(), name='maintenancerequest_list'),
    # path('maintenancerequests/<uuid:pk>/', MaintenanceRequestDetailView.as_view(), name='maintenancerequest_detail'),
    # path('maintenancerequests/new/', MaintenanceRequestCreateView.as_view(), name='maintenancerequest_create'),
    # path('maintenancerequests/<uuid:pk>/edit/', MaintenanceRequestUpdateView.as_view(), name='maintenancerequest_update'),
    # path('maintenancerequests/<uuid:pk>/delete/', MaintenanceRequestDeleteView.as_view(), name='maintenancerequest_delete'),

    # path('announcements/', AnnouncementListView.as_view(), name='announcement_list'),
    # path('announcements/<uuid:pk>/', AnnouncementDetailView.as_view(), name='announcement_detail'),
    # path('announcements/new/', AnnouncementCreateView.as_view(), name='announcement_create'),
    # path('announcements/<uuid:pk>/edit/', AnnouncementUpdateView.as_view(), name='announcement_update'),
    # path('announcements/<uuid:pk>/delete/', AnnouncementDeleteView.as_view(), name='announcement_delete'),

    # path('complaints/', ComplaintListView.as_view(), name='complaint_list'),
    # path('complaints/<uuid:pk>/', ComplaintDetailView.as_view(), name='complaint_detail'),
    # path('complaints/new/', ComplaintCreateView.as_view(), name='complaint_create'),
    # path('complaints/<uuid:pk>/edit/', ComplaintUpdateView.as_view(), name='complaint_update'),
    # path('complaints/<uuid:pk>/delete/', ComplaintDeleteView.as_view(), name='complaint_delete'),
]