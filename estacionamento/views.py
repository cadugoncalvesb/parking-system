from django.shortcuts import render
from entryRecord.models import EntryRecord
from exitRecord.models import ExitRecord
from parking.models import Parking

def home(request):
    total_entradas = EntryRecord.objects.count()
    total_saidas = ExitRecord.objects.count()
    vagas_ocupadas = total_entradas - total_saidas

    estacionamento = Parking.objects.first()
    total_vagas = estacionamento.totalVacancies if estacionamento else 0
    vagas_disponiveis = max(0, total_vagas - vagas_ocupadas)

    registros_abertos = EntryRecord.objects.filter(exitrecord__isnull=True)

    context = {
        'vagas_disponiveis': vagas_disponiveis,
        'total_vagas': total_vagas,
        'vagas_ocupadas': vagas_ocupadas,
        'exit_records': registros_abertos 
    }
    return render(request, 'estacionamento/home.html', context)
