# ADR 0006 — Iceberg taste track (local FS + SQLite catalog)

## Status
Accepted

## Context
Apache Iceberg is becoming the de-facto open table format for lakehouse architectures.
Including a working Iceberg demo shows awareness of the open-standards direction without
requiring a cloud object store or a Hive/Glue metastore.

## Decision
Use PyIceberg directly (not dlt's filesystem destination) with:

- **Catalog:** SQLite (`pyiceberg[sql-sqlite]`) at `data/iceberg/catalog.db` — zero
  external dependencies.
- **Storage:** local filesystem under `data/iceberg/warehouse/` (Parquet files).
- **Tables:** `meridian.orders` and `meridian.order_items`, written via `table.append()`
  on each pipeline run.
- **Schema evolution demo:** `update_schema().add_column("priority", StringType())` adds
  a new column without rewriting existing data files.
- **Time-travel demo:** snapshot metadata shows per-run `added-records` and
  `total-records`; querying an older snapshot ID is possible via PyIceberg's scan API.
- **DuckDB integration:** `iceberg_scan(metadata_location)` lets DuckDB query Iceberg
  tables directly — demonstrates the open-format interoperability story.

All schema fields declared as `required=False` (optional) to match PyArrow's default
nullability; PyIceberg 0.9+ enforces strict nullability matching between the Iceberg
schema and the Arrow table on `append()`.

## Consequences
- `data/iceberg/` is gitignored; regenerate with `make ingest-iceberg`.
- Running `make ingest-iceberg` twice is required before the time-travel test passes
  (needs ≥ 2 snapshots).
- Not integrated into the main Dagster pipeline — kept as an isolated taste track so it
  doesn't impose the DuckDB single-writer constraint on the rest of the stack.
