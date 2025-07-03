from django.views.generic import ListView, CreateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.timezone import now
from .models import ExitRecord, EntryRecord, PaymentType
import math
from django.db.models import OuterRef, Subquery, Exists
from decimal import Decimal
from django.shortcuts import render
from django import forms
from django.db.models import Sum, Count

class ExitRecordListView(ListView):
    model = ExitRecord
    template_name = 'exitRecord/list.html'
    context_object_name = 'exit_records'

    def get_queryset(self):
        return EntryRecord.objects.filter(
            ~Exists(ExitRecord.objects.filter(entryRecord=OuterRef('pk')))
        )

class ExitRecordCreateView(CreateView):
    model = ExitRecord
    fields = ['paymentType']
    template_name = 'exitRecord/form.html'
    success_url = reverse_lazy('exitrecord-list')

    def dispatch(self, request, *args, **kwargs):
        self.entry_record = get_object_or_404(EntryRecord, pk=self.kwargs['entry_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        entry = self.entry_record
        exit_time = now()

        final_value = self.request.session.get('valor')
        payment_type_id = self.request.POST.get('paymentType')

        form.instance.entryRecord = entry
        form.instance.exitDate = exit_time
        form.instance.finalValue = final_value
        form.instance.paymentType_id = payment_type_id

        # limpa a sessão
        self.request.session.pop('valor', None)
        self.request.session.pop('entry_id', None)

        return super().form_valid(form)

def confirmar_saida(request, entry_id):
    entry = get_object_or_404(EntryRecord, pk=entry_id)
    exit_time = now()
    duration = exit_time - entry.entryDate
    minutos = duration.total_seconds() / 60
    intervalos = math.ceil(minutos / 20)

    preco_por_intervalo = entry.vehicleType.valuePerVehicle  # pega do model
    valor = preco_por_intervalo * intervalos

    # Armazena temporariamente
    request.session['entry_id'] = entry.id
    request.session['valor'] = str(valor)

    formas_pagamento = PaymentType.objects.all()

    return render(request, 'exitRecord/confirmar_saida.html', {
        'entry': entry,
        'valor': valor,
        'formas_pagamento': formas_pagamento,
    })


class ReportForm(forms.Form):
    start_date = forms.DateField(label="Data inicial", required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label="Data final", required=True, widget=forms.DateInput(attrs={'type': 'date'}))

def caixa_report_view(request):
    form = ReportForm(request.GET or None)
    results = []
    total_value = 0
    total_count = 0
    total_by_payment = {}

    if form.is_valid():
        start = form.cleaned_data['start_date']
        end = form.cleaned_data['end_date']

        queryset = ExitRecord.objects.filter(exitDate__date__range=(start, end))

        results = queryset
        total_value = queryset.aggregate(total=Sum('finalValue'))['total'] or 0
        total_count = queryset.count()

        # Agrupado por forma de pagamento
        pagamentos = queryset.values('paymentType__description').annotate(total=Sum('finalValue'), count=Count('id'))
        total_by_payment = {p['paymentType__description']: {'valor': p['total'], 'qtd': p['count']} for p in pagamentos}

    context = {
        'form': form,
        'results': results,
        'total_value': total_value,
        'total_count': total_count,
        'total_by_payment': total_by_payment
    }
    return render(request, 'exitRecord/caixa_report.html', context)