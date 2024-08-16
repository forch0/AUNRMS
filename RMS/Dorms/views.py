from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Dorm, Room, Storage, StorageItem
from .forms import DormForm, RoomForm, StorageForm, StorageItemForm

# Views for Dorm

class DormListView(LoginRequiredMixin, ListView):
    model = Dorm
    template_name = 'dorms/dorm_list.html'
    context_object_name = 'dorms'

class DormDetailView(LoginRequiredMixin, DetailView):
    model = Dorm
    template_name = 'dorms/dorm_detail.html'
    context_object_name = 'dorm'

class DormCreateView(LoginRequiredMixin, CreateView):
    model = Dorm
    template_name = 'dorms/dorm_form.html'
    form_class = DormForm

class DormUpdateView(LoginRequiredMixin, UpdateView):
    model = Dorm
    template_name = 'dorms/dorm_form.html'
    form_class = DormForm

class DormDeleteView(LoginRequiredMixin, DeleteView):
    model = Dorm
    template_name = 'dorms/dorm_confirm_delete.html'
    success_url = reverse_lazy('dorm-list')

# Views for Room

class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'dorms/room_list.html'
    context_object_name = 'rooms'

class RoomDetailView(LoginRequiredMixin, DetailView):
    model = Room
    template_name = 'dorms/room_detail.html'
    context_object_name = 'room'

class RoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    template_name = 'dorms/room_form.html'
    form_class = RoomForm

class RoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    template_name = 'dorms/room_form.html'
    form_class = RoomForm

class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'dorms/room_confirm_delete.html'
    success_url = reverse_lazy('room-list')

# Views for Storage

class StorageListView(LoginRequiredMixin, ListView):
    model = Storage
    template_name = 'dorms/storage_list.html'
    context_object_name = 'storages'

class StorageDetailView(LoginRequiredMixin, DetailView):
    model = Storage
    template_name = 'dorms/storage_detail.html'
    context_object_name = 'storage'

class StorageCreateView(LoginRequiredMixin, CreateView):
    model = Storage
    template_name = 'dorms/storage_form.html'
    form_class = StorageForm

class StorageUpdateView(LoginRequiredMixin, UpdateView):
    model = Storage
    template_name = 'dorms/storage_form.html'
    form_class = StorageForm

class StorageDeleteView(LoginRequiredMixin, DeleteView):
    model = Storage
    template_name = 'dorms/storage_confirm_delete.html'
    success_url = reverse_lazy('storage-list')

# Views for StorageItem

class StorageItemListView(LoginRequiredMixin, ListView):
    model = StorageItem
    template_name = 'dorms/storageitem_list.html'
    context_object_name = 'storage_items'

class StorageItemDetailView(LoginRequiredMixin, DetailView):
    model = StorageItem
    template_name = 'dorms/storageitem_detail.html'
    context_object_name = 'storage_item'

class StorageItemCreateView(LoginRequiredMixin, CreateView):
    model = StorageItem
    template_name = 'dorms/storageitem_form.html'
    form_class = StorageItemForm

class StorageItemUpdateView(LoginRequiredMixin, UpdateView):
    model = StorageItem
    template_name = 'dorms/storageitem_form.html'
    form_class = StorageItemForm

class StorageItemDeleteView(LoginRequiredMixin, DeleteView):
    model = StorageItem
    template_name = 'dorms/storageitem_confirm_delete.html'
    success_url = reverse_lazy('storageitem-list')

def index(request):
    return HttpResponse("Welcome to Dorms Section.")

# 