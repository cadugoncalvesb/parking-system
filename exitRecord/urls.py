from django.urls import path
from .views import (ExitRecordCreateView, ExitRecordListView, confirmar_saida, caixa_report_view)

urlpatterns = [
    path('saida/list/', ExitRecordListView.as_view(), name='exitrecord-list'),
    path('saida/<int:entry_id>/registrar/', ExitRecordCreateView.as_view(), name='exitrecord-create'),
    path('saida/<int:entry_id>/confirmar/', confirmar_saida, name='exitrecord-confirmar'),
    path('relatorio-caixa/', caixa_report_view, name='relatorio-caixa'),
]