import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder

User = get_user_model()

class Tenant(models.Model):
    """
    Handles multi-tenancy for the platform.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class RawDataPayload(models.Model):
    """
    Immutable ledger of the exact untampered data payload/row as it arrived.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source_identifier = models.CharField(max_length=100, help_text="e.g., SAP_ALV, UTILITY_PORTAL, CONCUR_WEBHOOK")
    payload = models.JSONField(encoder=DjangoJSONEncoder, help_text="Exact untampered data payload/row")
    received_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.source_identifier} at {self.received_at}"

class NormalizedRecord(models.Model):
    """
    The standardized representation of the raw data.
    """
    SCOPE_CHOICES = [
        ('SCOPE_1', 'Scope 1'),
        ('SCOPE_2', 'Scope 2'),
        ('SCOPE_3', 'Scope 3'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('FLAGGED', 'Flagged'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='normalized_records')
    raw_payload = models.OneToOneField(RawDataPayload, on_delete=models.PROTECT, related_name='normalized_record')
    
    scope_category = models.CharField(max_length=20, choices=SCOPE_CHOICES)
    emission_source = models.CharField(max_length=100, help_text="e.g., electricity, flight, diesel_generator")
    
    raw_value = models.DecimalField(max_digits=19, decimal_places=4, null=True, blank=True)
    raw_unit = models.CharField(max_length=50, blank=True)
    standardized_value = models.DecimalField(max_digits=19, decimal_places=4, null=True, blank=True, help_text="Standardized to metric, e.g., tCO2e or kWh")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    suspicion_reason = models.TextField(blank=True, help_text="Populated if flagged during parsing")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tenant.name} - {self.scope_category} - {self.status}"

class AuditLog(models.Model):
    """
    Tracks every state change on a NormalizedRecord.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    record = models.ForeignKey(NormalizedRecord, on_delete=models.CASCADE, related_name='audit_logs')
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, help_text="User who made the change. Null for system actions.")
    action = models.CharField(max_length=255, help_text="e.g., STATUS_CHANGED_TO_APPROVED, PARSING_FLAGGED")
    
    # Granular edit tracking
    previous_value = models.CharField(max_length=255, null=True, blank=True, help_text="Specific value before edit")
    new_value = models.CharField(max_length=255, null=True, blank=True, help_text="Specific value after edit")
    
    previous_state = models.JSONField(encoder=DjangoJSONEncoder, null=True, blank=True)
    new_state = models.JSONField(encoder=DjangoJSONEncoder, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} on {self.record.id} at {self.timestamp}"
