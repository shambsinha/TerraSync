# Data Model Architecture

## Raw vs Normalized Separation
To meet enterprise audit and defensibility requirements, we employ a strict separation between incoming data and standardized metrics. 
- **`RawDataPayload`:** Serves as an immutable, append-only ledger. It stores the exact untampered JSON of the incoming row, along with the source identifier and ingestion timestamp. 
- **`NormalizedRecord`:** Represents the standardized, actionable data. It links directly to its parent `RawDataPayload` via a `OneToOneField`. This guarantees that an auditor or analyst can trace any standardized value (e.g., metric tons of CO2e) back to the exact character string that was submitted by the client system.

## Multi-Tenant Strategy
The platform is designed to handle multiple distinct organizations on a single deployment.
- **`Tenant` Model:** The root anchor for data isolation. Every `NormalizedRecord` is enforced with a mandatory foreign key to a `Tenant`. 

## Comprehensive Audit Trail
- **`AuditLog`:** ESG reporting requires proof of process. The `AuditLog` captures every state change on a `NormalizedRecord` (e.g., moving from `PENDING` to `APPROVED`, or being `FLAGGED` by a parser). 
- **Edit Tracking:** To satisfy strict transparency requirements, the `AuditLog` includes explicit `previous_value` and `new_value` fields. If an analyst modifies a value during the review process, both the original and the modified states are captured, providing a clear trail of human intervention before final approval. It also continues to store the full `previous_state` and `new_state` as JSON blobs for deep system recovery.