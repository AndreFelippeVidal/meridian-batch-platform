"""Top-level Dagster Definitions for the Meridian batch data platform."""

from pathlib import Path

import dagster as dg
import duckdb
from dagster_dbt import DbtCliResource
from dagster_dlt import DagsterDltResource

from orchestration.assets.ingest import meridian_dlt_assets
from orchestration.assets.quality import elementary_report_asset
from orchestration.assets.transform import TRANSFORM_DIR, meridian_dbt_assets

_DB_PATH = Path(__file__).parent.parent / "data" / "meridian.duckdb"


# ── Asset checks ──────────────────────────────────────────────────────────────

@dg.asset_check(asset="mart_marketplace_daily", blocking=True)
def check_daily_mart_has_rows(
    context: dg.AssetCheckExecutionContext,
) -> dg.AssetCheckResult:
    """Fail if the daily mart is empty after materialization."""
    con = duckdb.connect(str(_DB_PATH), read_only=True)
    count = con.execute(
        "SELECT count(*) FROM main_marts.mart_marketplace_daily"
    ).fetchone()[0]
    con.close()
    return dg.AssetCheckResult(passed=count > 0, metadata={"row_count": count})


@dg.asset_check(asset="fct_orders", blocking=True)
def check_fct_orders_has_rows(
    context: dg.AssetCheckExecutionContext,
) -> dg.AssetCheckResult:
    """Fail if fct_orders is empty after materialization."""
    con = duckdb.connect(str(_DB_PATH), read_only=True)
    count = con.execute("SELECT count(*) FROM main_marts.fct_orders").fetchone()[0]
    con.close()
    return dg.AssetCheckResult(passed=count > 0, metadata={"row_count": count})


# ── Jobs ──────────────────────────────────────────────────────────────────────

materialize_all_job = dg.define_asset_job(
    name="materialize_all",
    selection=dg.AssetSelection.all(),
    description="Ingest with dlt, then build all dbt staging + mart models end to end.",
)


# ── Top-level Definitions ─────────────────────────────────────────────────────

defs = dg.Definitions(
    assets=[meridian_dlt_assets, meridian_dbt_assets, elementary_report_asset],
    asset_checks=[check_daily_mart_has_rows, check_fct_orders_has_rows],
    jobs=[materialize_all_job],
    resources={
        "dlt": DagsterDltResource(),
        "dbt": DbtCliResource(
            project_dir=str(TRANSFORM_DIR),
            profiles_dir=str(TRANSFORM_DIR),
        ),
    },
)
