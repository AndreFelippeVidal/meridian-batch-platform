# ADR 0002 — DuckDB as local warehouse with dbt multi-target stub

## Status
Accepted

## Context
The platform needs a warehouse that runs entirely on a laptop with no cloud credentials, so
the portfolio can be demoed offline. The dbt project must also be portable to Snowflake when
a hiring manager wants to see a production-grade target.

## Decision
Use DuckDB as the primary warehouse target. A Snowflake stub is declared in `profiles.yml`
(inactive by default, activated by setting `target: snowflake` and populating env vars).
dbt `threads: 1` is fixed for DuckDB because Elementary's incremental models require a
single writer connection.

## Consequences
- Zero cost, zero setup — `make ingest && make transform` works on any Mac/Linux without
  cloud auth.
- Elementary and dbt-duckdb impose the single-thread constraint; this is acceptable for a
  500-customer, 2 000-order synthetic dataset.
- Snowflake stub means the dbt project is structurally ready for a real warehouse swap
  (change `target:` + env vars; no model SQL changes required).
