from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from ingestion.views import (
    SAPUploadView, UtilityUploadView, ConcurWebhookView,
    NormalizedRecordListView, NormalizedRecordUpdateView
)

def root_view(request):
    return JsonResponse({
        "status": "online",
        "message": "TerraSync ESG API is live.",
        "endpoints": {
            "records": "/api/records/",
            "ingest_sap": "/api/ingest/sap/",
            "ingest_utility": "/api/ingest/utility/",
            "ingest_concur": "/api/ingest/concur/"
        }
    })

urlpatterns = [
    path('', root_view),
    path('admin/', admin.site.urls),
    path('api/records/', NormalizedRecordListView.as_view(), name='record-list'),
# ... existing paths ...
    path('api/records/<uuid:pk>/', NormalizedRecordUpdateView.as_view(), name='record-update'),
    path('api/ingest/sap/', SAPUploadView.as_view(), name='sap-upload'),
    path('api/ingest/utility/', UtilityUploadView.as_view(), name='utility-upload'),
    path('api/ingest/concur/', ConcurWebhookView.as_view(), name='concur-webhook'),
]
