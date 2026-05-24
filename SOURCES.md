# Data Sources & Assumptions

This document outlines the expected shapes of our integration points, our parser assumptions, and potential production failure modes.

## 1. SAP Procurement (Scope 1 Fuel)
- **Realistic Shape:** CSV exports containing German standard headers such as `BUKRS` (Company Code), `MENGE` (Quantity), and `MEINS` (Base Unit of Measure).
- **Assumptions:** We assume quantities are cleanly formatted standard decimals and that units are recognizable identifiers like `L` or `GAL`.
- **Edge Cases:** Real SAP exports often utilize European number formatting (e.g., `1.000,50` instead of `1000.50`), which our prototype parser does not currently sanitize. Unrecognized localized units will instantly flag the row.

## 2. Utility Portals (Scope 2 Electricity)
- **Realistic Shape:** CSV containing `Meter ID`, `Start Date`, `End Date`, `Total kWh`, and `Peak Demand kW`.
- **Assumptions:** Dates strictly follow `YYYY-MM-DD`. We assume `Total kWh` is a positive representation of actual usage.
- **Edge Cases:** The parser handles basic disproportionate load checks, but production data often includes bill estimations, negative values for billing corrections/credits, or missing peak demand values entirely.

## 3. Concur Webhooks (Scope 3 Corporate Travel)
- **Realistic Shape:** JSON payload with `employee_id`, `origin_iata`, `destination_iata`, and `cabin_class`. Crucially, distance is not provided by the source.
- **Assumptions:** IATA codes map 1:1 to physical airports where great-circle distance algorithms can be applied. We use a heavily mocked internal dictionary for testing.
- **Edge Cases:** Multi-leg flights, stopovers, and code-share anomalies are not accounted for. Any missing or invalid IATA code in our internal lookup immediately flags the record for manual analyst review.