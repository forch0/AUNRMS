from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,  PermissionRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Dorm, Room, Storage, StorageItem
from .forms import *
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

def index(request):
    return HttpResponse("Welcome to Dorms Section.")

# Dorm Views
class DormListView(LoginRequiredMixin, ListView):
    model = Dorm
    template_name = 'dorms/dorm_list.html'
    context_object_name = 'dorms'
    paginate_by = 10  # Optional: add pagination if needed

class DormCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Dorm
    form_class = DormForm
    template_name = 'dorms/dorm_form.html'
    success_url = reverse_lazy('dorm_list')
    permission_required = 'dorms.add_dorm'
    raise_exception = True

class DormUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Dorm
    form_class = DormForm
    template_name = 'dorms/dorm_form.html'
    success_url = reverse_lazy('dorm_list')
    permission_required = 'dorms.change_dorm'
    raise_exception = True

class DormDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Dorm
    template_name = 'dorms/dorm_confirm_delete.html'
    success_url = reverse_lazy('dorm_list')
    permission_required = 'dorms.delete_dorm'
    raise_exception = True

# Room Views
class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'dorms/room_list.html'
    context_object_name = 'rooms'
    paginate_by = 10  # Optional: add pagination if needed

class RoomCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'dorms/room_form.html'
    success_url = reverse_lazy('room_list')
    permission_required = 'dorms.add_room'
    raise_exception = True

class RoomUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'dorms/room_form.html'
    success_url = reverse_lazy('room_list')
    permission_required = 'dorms.change_room'
    raise_exception = True

class RoomDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Room
    template_name = 'dorms/room_confirm_delete.html'
    success_url = reverse_lazy('room_list')
    permission_required = 'dorms.delete_room'
    raise_exception = True

# Storage Views
class StorageListView(LoginRequiredMixin, ListView):
    model = Storage
    template_name = 'dorms/storage_list.html'
    context_object_name = 'storages'
    paginate_by = 10  # Optional: add pagination if needed

class StorageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Storage
    form_class = StorageForm
    template_name = 'dorms/storage_form.html'
    success_url = reverse_lazy('storage_list')
    permission_required = 'dorms.add_storage'
    raise_exception = True

class StorageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Storage
    form_class = StorageForm
    template_name = 'dorms/storage_form.html'
    success_url = reverse_lazy('storage_list')
    permission_required = 'dorms.change_storage'
    raise_exception = True

class StorageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Storage
    template_name = 'dorms/storage_confirm_delete.html'
    success_url = reverse_lazy('storage_list')
    permission_required = 'dorms.delete_storage'
    raise_exception = True

# StorageItem Views
class StorageItemListView(LoginRequiredMixin, ListView):
    model = StorageItem
    template_name = 'dorms/storage_item_list.html'
    context_object_name = 'storage_items'
    paginate_by = 10  # Optional: add pagination if needed

class StorageItemCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = StorageItem
    form_class = StorageItemForm
    template_name = 'dorms/storage_item_form.html'
    success_url = reverse_lazy('storage_item_list')
    permission_required = 'dorms.add_storageitem'
    raise_exception = True

class StorageItemUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = StorageItem
    form_class = StorageItemForm
    template_name = 'dorms/storage_item_form.html'
    success_url = reverse_lazy('storage_item_list')
    permission_required = 'dorms.change_storageitem'
    raise_exception = True

class StorageItemDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = StorageItem
    template_name = 'dorms/storage_item_confirm_delete.html'
    success_url = reverse_lazy('storage_item_list')
    permission_required = 'dorms.delete_storageitem'
    raise_exception = True


class StorageItemApproveView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'dorms.change_storageitem'
    raise_exception = True

    def get(self, request, *args, **kwargs):
        storage_item_id = kwargs.get('pk')
        storage_item = get_object_or_404(StorageItem, id=storage_item_id)
        form = StorageItemApprovalForm(instance=storage_item)
        
        return render(request, 'dorms/storage_item_approve.html', {
            'form': form,
            'storage_item': storage_item
        })

    def post(self, request, *args, **kwargs):
        storage_item_id = kwargs.get('pk')
        storage_item = get_object_or_404(StorageItem, id=storage_item_id)
        form = StorageItemApprovalForm(request.POST, instance=storage_item)
        
        if form.is_valid():
            staff_member = request.user  # Assuming the logged-in user is a staff member
            storage_item.approve(staff_member)
            return redirect('storage_item_list')
        
        return render(request, 'dorms/storage_item_approve.html', {
            'form': form,
            'storage_item': storage_item
        })