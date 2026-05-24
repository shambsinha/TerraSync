import csv
import io
from datetime import datetime
from decimal import Decimal
from .models import RawDataPayload, NormalizedRecord, AuditLog

def process_sap_csv(file_obj, tenant):
    decoded_file = file_obj.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(decoded_file))
    
    # Explicit mapping of German SAP ALV headers to internal keys
    SAP_HEADER_MAP = {
        'BUKRS': 'company_code',
        'MENGE': 'quantity',
        'MEINS': 'unit',
        'GSBER': 'business_area'
    }
    
    records_created = 0
    for row in reader:
        # Map raw row to internal normalized keys
        mapped_data = {SAP_HEADER_MAP.get(k, k): v for k, v in row.items()}
        
        raw = RawDataPayload.objects.create(
            source_identifier='SAP_ALV',
            payload=row # Store the UNTAMPERED row as required
        )
        
        quantity_str = mapped_data.get('quantity')
        unit_str = mapped_data.get('unit')
        
        status = 'PENDING'
        suspicion_reason = ''
        standardized_value = None
        
        if not unit_str:
            status = 'FLAGGED'
            suspicion_reason = 'Missing unit of measure (MEINS)'
        else:
            try:
                raw_val = Decimal(quantity_str) if quantity_str else Decimal('0')
                if unit_str.upper() == 'L':
                    standardized_value = raw_val
                elif unit_str.upper() == 'GAL':
                    standardized_value = raw_val * Decimal('3.78541')
                else:
                    status = 'FLAGGED'
                    suspicion_reason = f'Unrecognized unit: {unit_str}'
            except Exception:
                status = 'FLAGGED'
                suspicion_reason = f'Invalid quantity: {quantity_str}'

        norm_record = NormalizedRecord.objects.create(
            tenant=tenant,
            raw_payload=raw,
            scope_category='SCOPE_1',
            emission_source='Fuel (Procurement)',
            raw_value=Decimal(quantity_str) if quantity_str and quantity_str.replace('.','',1).isdigit() else None,
            raw_unit=unit_str or '',
            standardized_value=standardized_value,
            status=status,
            suspicion_reason=suspicion_reason
        )
        AuditLog.objects.create(
            record=norm_record,
            action='SYSTEM_PARSED_SAP_CSV'
        )
        records_created += 1
    return records_created


def process_utility_csv(file_obj, tenant):
    decoded_file = file_obj.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(decoded_file))
    
    records_created = 0
    for row in reader:
        raw = RawDataPayload.objects.create(
            source_identifier='UTILITY_PORTAL',
            payload=row
        )
        
        start_date_str = row.get('Start Date')
        end_date_str = row.get('End Date')
        total_kwh_str = row.get('Total kWh')
        peak_kw_str = row.get('Peak Demand kW')
        
        status = 'PENDING'
        suspicion_reason = ''
        daily_average = None
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            days = (end_date - start_date).days
            
            total_kwh = Decimal(total_kwh_str) if total_kwh_str else Decimal('0')
            peak_kw = Decimal(peak_kw_str) if peak_kw_str else Decimal('0')
            
            if days > 0:
                daily_average = total_kwh / Decimal(days)
            else:
                status = 'FLAGGED'
                suspicion_reason = 'Invalid date range (days <= 0)'
                
            if days > 0 and peak_kw > 0:
                max_possible = peak_kw * Decimal(days) * Decimal('24')
                if total_kwh > max_possible:
                    status = 'FLAGGED'
                    suspicion_reason = 'Total kWh exceeds theoretical maximum based on Peak Demand'
                elif total_kwh < peak_kw * Decimal('0.01'):
                    status = 'FLAGGED'
                    suspicion_reason = 'Disproportionately low kWh for stated Peak Demand'
        except Exception as e:
            status = 'FLAGGED'
            suspicion_reason = f'Parsing error: {str(e)}'
            
        norm_record = NormalizedRecord.objects.create(
            tenant=tenant,
            raw_payload=raw,
            scope_category='SCOPE_2',
            emission_source='Electricity',
            raw_value=Decimal(total_kwh_str) if total_kwh_str and total_kwh_str.replace('.','',1).isdigit() else None,
            raw_unit='kWh',
            standardized_value=daily_average,
            status=status,
            suspicion_reason=suspicion_reason
        )
        AuditLog.objects.create(
            record=norm_record,
            action='SYSTEM_PARSED_UTILITY_CSV'
        )
        records_created += 1
    return records_created


def process_concur_webhook(payload, tenant):
    raw = RawDataPayload.objects.create(
        source_identifier='CONCUR_WEBHOOK',
        payload=payload
    )
    
    origin = payload.get('origin_iata', '').upper()
    dest = payload.get('destination_iata', '').upper()
    cabin = payload.get('cabin_class', '').lower()
    
    MOCK_DISTANCES = {
        ('JFK', 'LHR'): 5540,
        ('LHR', 'JFK'): 5540,
        ('SFO', 'JFK'): 4150,
        ('JFK', 'SFO'): 4150,
        ('FRA', 'LHR'): 656,
        ('LHR', 'FRA'): 656,
    }
    
    status = 'PENDING'
    suspicion_reason = ''
    standardized_value = None
    
    distance = MOCK_DISTANCES.get((origin, dest))
    
    if not distance:
        status = 'FLAGGED'
        suspicion_reason = f'Unrecognized or unsupported IATA route: {origin} to {dest}'
    else:
        factors = {
            'economy': Decimal('0.15'),
            'business': Decimal('0.30'),
            'first': Decimal('0.45')
        }
        ef = factors.get(cabin)
        if not ef:
            status = 'FLAGGED'
            suspicion_reason = f'Unrecognized cabin class: {cabin}'
        else:
            standardized_value = Decimal(distance) * ef 
            
    norm_record = NormalizedRecord.objects.create(
        tenant=tenant,
        raw_payload=raw,
        scope_category='SCOPE_3',
        emission_source='Corporate Travel (Flight)',
        raw_value=None,
        raw_unit='route',
        standardized_value=standardized_value,
        status=status,
        suspicion_reason=suspicion_reason
    )
    AuditLog.objects.create(
        record=norm_record,
        action='SYSTEM_PARSED_CONCUR_WEBHOOK'
    )
    
    return norm_record.id