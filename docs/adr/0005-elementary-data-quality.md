# ADR 0005 — Elementary for data quality observability

## Status
Accepted

## Context
dbt generic tests (unique, not_null, relationships, accepted_values) cover structural
correctness but don't produce a human-readable observability report. A portfolio project
needs to show awareness of data quality tooling beyond raw test counts.

## Decision
Add `elementary-data` as a dbt package (runs as `on-run-end` hooks during `dbt build`)
and as a Python package (`elementary-data[duckdb]`) for the `edr report` CLI.

- `elementary` profile added to `transform/profiles.yml` — required by `edr` to locate
  the warehouse independent of the dbt project profile.
- `edr report` writes `transform/edr_target/elementary_report.html`.
- A Dagster `elementary_report` asset (group: quality) shells out `edr report` after the
  mart assets materialise, so the report is always fresh.
- `tests/test_data_quality.py` includes a bad-row roundtrip: injects a negative-GMV row,
  asserts `dbt test` catches it, then cleans up — proving the gate works end-to-end.

**Constraint:** DuckDB only allows a single writer. Elementary runs many incremental models
concurrently, so `threads: 1` is required in `profiles.yml`. Using threads > 1 causes
`IO Error: Conflicting lock` failures.

## Consequences
- The HTML report is gitignored (`transform/edr_target/`) but reproducible with
  `make edr-report`.
- Elementary adds ~30 dbt models to the project (its own schema); these are hidden from
  the Dagster lineage graph via the default translator.
