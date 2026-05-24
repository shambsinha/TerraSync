# Architectural Decisions

## SAP Ingestion: ALV CSV over IDocs
We chose to accept CSV file uploads simulating SAP ALV Grid exports instead of building direct SAP IDoc/RFC integrations. 
**Reasoning:** In enterprise environments, establishing direct backend integration with legacy SAP ECC or S/4HANA instances requires extensive security reviews, firewall changes, and SAP Basis team involvement, often taking months. ALV Grid exports are a ubiquitous end-user feature; allowing CSV uploads removes the IT bottleneck and empowers sustainability teams to onboard data immediately.

## Frontend UI: React over Server-Side Templates
We built the analyst dashboard using React, Vite, and Tailwind CSS instead of traditional Django server-side rendered templates.
**Reasoning:** The review experience demands high interactivity. Analysts need to rapidly sort, filter, and compare data side-by-side (via the Record Drawer) without full-page reloads. A Single Page Application (SPA) architecture provides the necessary state management for instant UI feedback when approving or rejecting flagged records.

## Handling Utility Billing Overlaps
Utility bills frequently span across calendar month boundaries (e.g., a bill from April 14 to May 12).
**Reasoning:** To normalize this data for monthly or quarterly Scope 2 reporting, our parser calculates a daily average by dividing the `Total kWh` by the exact number of days between the start and end dates. This standardized daily rate allows downstream aggregation logic to accurately apportion consumption to specific calendar months. Note: In this version, we have **ignored complex tariff structures** (time-of-use, seasonal rates) to maintain sprint velocity.

## Scope Clarifications
- **Corporate Travel:** This prototype exclusively handles **flights**. We have intentionally **ignored hotels and ground transport** as their emission factors and data shapes vary significantly and require separate normalization streams.
- **Utility Data:** As noted above, we assume a flat consumption rate per billing period and do not account for tiered pricing or peak-demand penalties in the normalization logic.

## Questions for the Product Manager
1. **Utility Tariff Normalization:** How should the platform handle complex tariff structures (e.g., peak vs. off-peak rates) when clients require high-precision financial-to-carbon reconciliation?
2. **Compliance Workflows:** Are strict **maker-checker** (dual authorization) workflows required for final data approval to satisfy specific regulatory frameworks (e.g., CSRD or SEC requirements)?