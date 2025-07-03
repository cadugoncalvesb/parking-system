from django.urls import path
from .views import (
    VehicleTypeListView, VehicleTypeDetailView,
    VehicleTypeCreateView, VehicleTypeUpdateView, VehicleTypeDeleteView
)

urlpatterns = [
    path('', VehicleTypeListView.as_view(), name='vehicletype-list'),
    path('<int:pk>/', VehicleTypeDetailView.as_view(), name='vehicletype-detail'),
    path('create/', VehicleTypeCreateView.as_view(), name='vehicletype-create'),
    path('<int:pk>/update/', VehicleTypeUpdateView.as_view(), name='vehicletype-update'),
    path('<int:pk>/delete/', VehicleTypeDeleteView.as_view(), name='vehicletype-delete'),
]
