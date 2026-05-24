export interface RawDataPayload {
  id: string;
  source_identifier: string;
  payload: Record<string, any>;
  received_at: string;
}

export interface NormalizedRecord {
  id: string;
  scope_category: 'SCOPE_1' | 'SCOPE_2' | 'SCOPE_3';
  emission_source: string;
  raw_value: number | null;
  raw_unit: string;
  standardized_value: number | null;
  status: 'PENDING' | 'APPROVED' | 'REJECTED' | 'FLAGGED';
  suspicion_reason?: string;
  created_at: string;
  raw_payload?: RawDataPayload;
}
