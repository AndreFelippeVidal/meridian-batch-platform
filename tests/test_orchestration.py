"""Verify the Dagster orchestration skeleton: dlt assets materialize successfully."""

from pathlib import Path

import dlt
import duckdb
import pytest
from dagster import AssetExecutionContext, materialize
from dagster_dlt import DagsterDltResource, dlt_assets

from ingestion.meridian_source import meridian_source


@pytest.fixture()
def isolated_pipeline(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dlt.Pipeline:
    """Fresh DuckDB pipeline with isolated dlt state directory."""
    monkeypatch.setenv("DLT_DATA_DIR", str(tmp_path / "dlt_data"))
    return dlt.pipeline(
        pipeline_name="test_meridian_dag",
        destination=dlt.destinations.duckdb(str(tmp_path / "test.duckdb")),
        dataset_name="raw",
    )


def test_dlt_assets_materialize(isolated_pipeline: dlt.Pipeline, tmp_path: Path) -> None:
    @dlt_assets(
        dlt_source=meridian_source(),
        dlt_pipeline=isolated_pipeline,
        name="meridian_raw_test",
        group_name="raw",
    )
    def _test_dlt_assets(context: AssetExecutionContext, dlt: DagsterDltResource) -> object:
        yield from dlt.run(context=context)

    result = materialize(
        [_test_dlt_assets],
        resources={"dlt": DagsterDltResource()},
    )
    assert result.success, "dlt Dagster assets did not materialize successfully"

    db_path = str(tmp_path / "test.duckdb")
    con = duckdb.connect(db_path, read_only=True)
    tables = {
        r[0]
        for r in con.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='raw'"
        ).fetchall()
    }
    con.close()
    assert "customers" in tables
    assert "orders" in tables
    assert "payments" in tables
