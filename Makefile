.PHONY: setup lint fmt typecheck test run clean ingest verify-ingest dagster-dev \
        dbt-deps transform dbt-test dbt-docs materialize-all
# uv handles venv + lockfile + installs. https://docs.astral.sh/uv/

setup:          ## create venv, install deps, install pre-commit hooks
	uv sync
	uv run pre-commit install

lint:           ## lint without changing files
	uv run ruff check .

fmt:            ## auto-format + autofix
	uv run ruff format .
	uv run ruff check --fix .

typecheck:      ## static types
	uv run mypy src

test:           ## run tests with coverage
	uv run pytest

run:            ## run the project entrypoint
	uv run python -m project

ingest:         ## load Meridian domain data into DuckDB raw schema
	uv run python -m ingestion.pipeline

verify-ingest:  ## run ingestion pytest gate
	uv run pytest tests/test_ingestion.py -v

dagster-dev:    ## launch Dagster UI (Ctrl-C to stop)
	uv run dagster dev -m orchestration.definitions

dbt-deps:       ## install dbt packages (dbt_utils, dbt_expectations, elementary)
	cd transform && uv run dbt deps

transform:      ## run dbt build — models + tests
	cd transform && uv run dbt build --profiles-dir .

dbt-test:       ## run dbt tests only
	cd transform && uv run dbt test --profiles-dir .

dbt-docs:       ## generate dbt docs (open target/index.html to browse)
	cd transform && uv run dbt docs generate --profiles-dir . && uv run dbt docs serve --profiles-dir .

materialize-all: ## materialize full Dagster graph — dlt raw → dbt staging → marts
	uv run dagster asset materialize --select '*' -m orchestration.definitions

clean:
	rm -rf .venv .pytest_cache .mypy_cache .ruff_cache __pycache__ */__pycache__
