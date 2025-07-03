from django.urls import path
from .views import (
    EntryRecordCreateView, EntryRecordListView, EntryRecordUpdateView
)

urlpatterns = [
    path('', EntryRecordCreateView.as_view(), name='entryrecord-create'),
    path('list/', EntryRecordListView.as_view(), name='entryrecord-list'),
    path('<int:pk>/update/', EntryRecordUpdateView.as_view(), name='entryrecord-update'),
]