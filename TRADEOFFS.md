# Intentional Tradeoffs

For the purposes of this 4-day prototype sprint, several compromises were intentionally made to prioritize core architectural clarity and immediate user value.

## 1. Skipped Asynchronous Processing (Celery/Redis)
**Tradeoff:** Currently, CSV ingestion and parsing occur synchronously within the Django view request-response cycle. 
**Impact:** While sufficient for prototype datasets, uploading massive multi-gigabyte files in production will block the web thread and cause HTTP timeouts. We skipped adding Celery/Redis to minimize infrastructure overhead, deferring scalable background processing to a future iteration.

## 2. Skipped Full Role-Based Access Control (RBAC)
**Tradeoff:** The system assumes a generic user context for audit logs, but lacks strict permission enforcement via robust RBAC.
**Impact:** In a real deployment, strict boundaries must exist between "Data Submitters", "Review Analysts", and "External Auditors". Building comprehensive permission matrices and group policies was deferred to maintain velocity on the data pipelines.

## 3. Skipped Real-Time Emission Factor API Integration
**Tradeoff:** Emission factors (e.g., CO2e per km flown) are hardcoded into static lookup dictionaries in the parsing logic.
**Impact:** Production ESG systems must rely on dynamically updated, scientifically rigorous databases (like the EPA or DEFRA APIs). Live integration introduces network latency, potential downtime, and caching complexities that we bypassed to ensure consistent prototype demonstration.