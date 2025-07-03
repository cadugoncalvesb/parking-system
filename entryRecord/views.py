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

class EntryRecordCreateView(CreateView):
    model = EntryRecord
    fields = ['plate', 'vehicleType']
    template_name = 'entryRecord/form.html'
    success_url = reverse_lazy('entryrecord-list')

    def form_valid(self, form):
        # Garante que a verificação e a gravação usem o mesmo snapshot do banco
        with transaction.atomic():
            estacionamento = (
                Parking.objects
                .select_for_update()   # bloqueia a linha ─ evita corrida de duas requisições simultâneas
                .first()
            )
            if not estacionamento:
                messages.error(
                    self.request,
                    "Configuração do estacionamento não encontrada. Cadastre o total de vagas antes."
                )
                return redirect(self.success_url)

            # Quantos veículos estão dentro agora?
            vagas_ocupadas = EntryRecord.objects.filter(exitrecord__isnull=True).count()

            if vagas_ocupadas >= estacionamento.totalVacancies:
                messages.warning(
                    self.request,
                    "Estacionamento lotado — todas as vagas estão ocupadas."
                )
                return redirect(self.success_url)

            # Ainda há vaga ─ salva normalmente
            response = super().form_valid(form)
            messages.success(self.request, "Entrada registrada com sucesso!")
            return response

class EntryRecordUpdateView(UpdateView):
    model = EntryRecord
    fields = ['plate', 'vehicleType']
    template_name = 'entryRecord/form.html'
    success_url = reverse_lazy('entryrecord-list')