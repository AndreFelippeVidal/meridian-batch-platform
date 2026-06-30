# ADR 0004 — Dagster as orchestrator with software-defined assets

## Status
Accepted

## Context
The pipeline has three distinct phases (ingest → transform → quality report) that need
observable, re-runnable units with dependency tracking. The orchestrator must integrate
natively with both dlt and dbt without adapter boilerplate.

## Decision
Use Dagster's software-defined asset (SDA) model:

- `@dlt_assets` (dagster-dlt) wraps the dlt pipeline → produces the 5 raw assets.
- `@dbt_assets` (dagster-dbt) wraps the dbt project manifest → produces staging + mart
  assets with full column-level lineage.
- `@dg.asset` wraps the `edr report` CLI → produces the Elementary quality report asset.
- Two `@dg.asset_check` definitions gate `mart_marketplace_daily` and `fct_orders` on
  non-empty row counts.
- A `materialize_all` job selects all assets for a single-command end-to-end run.

**Critical implementation note:** `from __future__ import annotations` must NOT appear in
any file containing Dagster asset decorators. PEP 563 stringifies type annotations at
parse time, breaking Dagster's runtime `isinstance` check on `AssetExecutionContext`.

## Consequences
- Full lineage is visible in the Dagster UI from raw entities through marts — useful as a
  portfolio demo artifact.
- `DbtCliResource` (not the deprecated `DagsterDbtResource`) is the correct class in
  dagster-dbt ≥ 0.25.
- The `dbt parse` step must run before `dagster dev` to generate `manifest.json`;
  `DbtProject` handles this automatically in dev mode.
