from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import EntryRecord
from parking.models import Parking
from django.db import transaction
from django.contrib import messages
from django.shortcuts import redirect

class EntryRecordListView(ListView):
    model = EntryRecord
    template_name = 'entryRecord/list.html'
    context_object_name = 'entry_records'
    ordering = ['-entryDate']

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(plate__icontains=query[:7])  
        return queryset
    
class EntryRecordCreateView(CreateView):
    model = EntryRecord
    fields = ['plate', 'vehicleType']
    template_name = 'entryRecord/form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        with transaction.atomic():
            estacionamento = (
                Parking.objects
                .select_for_update()   
                .first()
            )
            if not estacionamento:
                messages.error(
                    self.request,
                    "Configuração do estacionamento não encontrada. Cadastre o total de vagas antes."
                )
                return redirect(self.success_url)

            vagas_ocupadas = EntryRecord.objects.filter(exitrecord__isnull=True).count()

            if vagas_ocupadas >= estacionamento.totalVacancies:
                messages.warning(
                    self.request,
                    "Estacionamento lotado — todas as vagas estão ocupadas."
                )
                return redirect(self.success_url)

            response = super().form_valid(form)
            messages.success(self.request, "Entrada registrada com sucesso!")
            return response

class EntryRecordUpdateView(UpdateView):
    model = EntryRecord
    fields = ['plate', 'vehicleType']
    template_name = 'entryRecord/form.html'
    success_url = reverse_lazy('entryrecord-list')