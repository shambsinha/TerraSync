from django.contrib import admin
from django.urls import path
from ingestion.views import (
    SAPUploadView, UtilityUploadView, ConcurWebhookView,
    NormalizedRecordListView, NormalizedRecordUpdateView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/records/', NormalizedRecordListView.as_view(), name='record-list'),
    path('api/records/<uuid:pk>/', NormalizedRecordUpdateView.as_view(), name='record-update'),
    path('api/ingest/sap/', SAPUploadView.as_view(), name='sap-upload'),
    path('api/ingest/utility/', UtilityUploadView.as_view(), name='utility-upload'),
    path('api/ingest/concur/', ConcurWebhookView.as_view(), name='concur-webhook'),
]
