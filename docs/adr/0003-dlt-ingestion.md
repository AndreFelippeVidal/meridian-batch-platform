# ADR 0003 — dlt for declarative ingestion

## Status
Accepted

## Context
Raw data needs to land in the warehouse in a way that is repeatable, schema-aware, and
demonstrates incremental loading without bespoke ETL code.

## Decision
Use `dlt` (dlthub) with a `@dlt.source` / `@dlt.resource` pattern.

- `orders` and `payments` use `write_disposition="merge"` with `primary_key` + `cursor_field`
  so re-running the pipeline never duplicates rows.
- `customers`, `products`, `order_items` use `write_disposition="replace"` (full refresh
  each run — they are static for this synthetic dataset).
- Destination: `dlt.destinations.duckdb("data/meridian.duckdb")`, dataset `raw`.

dlt handles schema inference, `_dlt_load_id` metadata columns, and pipeline state tracking
in `.dlt/` (gitignored).

## Consequences
- Ingestion is deterministic and idempotent — `pytest tests/test_ingestion.py` verifies
  zero duplicate rows on second run.
- The `@dlt.source` abstraction makes the source swappable to a real API with a one-line
  change to the resource generator.
- `.dlt/` pipeline state must not be committed (handled in `.gitignore`).
