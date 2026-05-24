from rest_framework import serializers
from .models import Tenant, RawDataPayload, NormalizedRecord, AuditLog

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'

class RawDataPayloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawDataPayload
        fields = '__all__'

class NormalizedRecordSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(read_only=True)
    raw_payload = RawDataPayloadSerializer(read_only=True)
    
    class Meta:
        model = NormalizedRecord
        fields = '__all__'

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'
