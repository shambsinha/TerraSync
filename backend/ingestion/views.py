from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Tenant, NormalizedRecord, AuditLog
from .parsers import process_sap_csv, process_utility_csv, process_concur_webhook
from django.db import transaction

from .serializers import NormalizedRecordSerializer

class NormalizedRecordListView(generics.ListAPIView):
    queryset = NormalizedRecord.objects.all().select_related('raw_payload', 'tenant')
    serializer_class = NormalizedRecordSerializer
    
class NormalizedRecordUpdateView(generics.UpdateAPIView):
    queryset = NormalizedRecord.objects.all()
    serializer_class = NormalizedRecordSerializer
    
    def perform_update(self, serializer):
        instance = self.get_object()
        old_status = instance.status
        old_value = str(instance.standardized_value)
        
        with transaction.atomic():
            new_instance = serializer.save()
            new_status = new_instance.status
            new_value = str(new_instance.standardized_value)
            
            # Logic to handle audit logging for edits vs status changes
            action = f"STATUS_CHANGED_{old_status}_TO_{new_status}"
            
            AuditLog.objects.create(
                record=new_instance,
                actor=self.request.user if self.request.user.is_authenticated else None,
                action=action,
                previous_value=old_value if old_value != new_value else None,
                new_value=new_value if old_value != new_value else None,
                previous_state={"status": old_status, "value": old_value},
                new_state={"status": new_status, "value": new_value}
            )

class SAPUploadView(APIView):
# ... existing code ...
    def post(self, request):
        tenant_id = request.data.get('tenant_id')
        file_obj = request.FILES.get('file')
        if not file_obj or not tenant_id:
            return Response({'error': 'Missing file or tenant_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            tenant = Tenant.objects.get(id=tenant_id)
        except Tenant.DoesNotExist:
            return Response({'error': 'Tenant not found'}, status=status.HTTP_404_NOT_FOUND)
            
        records_created = process_sap_csv(file_obj, tenant)
        return Response({'message': f'Successfully processed {records_created} SAP records'})

class UtilityUploadView(APIView):
    def post(self, request):
        tenant_id = request.data.get('tenant_id')
        file_obj = request.FILES.get('file')
        if not file_obj or not tenant_id:
            return Response({'error': 'Missing file or tenant_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            tenant = Tenant.objects.get(id=tenant_id)
        except Tenant.DoesNotExist:
            return Response({'error': 'Tenant not found'}, status=status.HTTP_404_NOT_FOUND)
            
        records_created = process_utility_csv(file_obj, tenant)
        return Response({'message': f'Successfully processed {records_created} Utility records'})

class ConcurWebhookView(APIView):
    def post(self, request):
        tenant_id = request.data.get('tenant_id') or request.query_params.get('tenant_id')
        payload = request.data
        if not payload or not tenant_id:
            return Response({'error': 'Missing payload or tenant_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            tenant = Tenant.objects.get(id=tenant_id)
        except Tenant.DoesNotExist:
            return Response({'error': 'Tenant not found'}, status=status.HTTP_404_NOT_FOUND)
            
        record_id = process_concur_webhook(payload, tenant)
        return Response({'message': 'Webhook processed successfully', 'record_id': record_id})