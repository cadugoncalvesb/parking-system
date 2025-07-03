from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import VehicleType

class VehicleTypeListView(ListView):
    model = VehicleType
    template_name = 'vehicleType/list.html'
    context_object_name = 'vehicle_types'  

class VehicleTypeDetailView(DetailView):
    model = VehicleType
    template_name = 'vehicleType/detail.html'
    context_object_name = 'vehicle_type'  

class VehicleTypeCreateView(CreateView):
    model = VehicleType
    fields = ['category', 'valuePerVehicle']
    template_name = 'vehicleType/form.html'
    success_url = reverse_lazy('vehicletype-list')

class VehicleTypeUpdateView(UpdateView):
    model = VehicleType
    fields = ['category', 'valuePerVehicle']
    template_name = 'vehicleType/form.html'
    success_url = reverse_lazy('vehicletype-list')

class VehicleTypeDeleteView(DeleteView):
    model = VehicleType
    template_name = 'vehicleType/confirm_delete.html'
    success_url = reverse_lazy('vehicletype-list')
   
