"""Dagster asset that runs the Elementary edr report and surfaces it as an asset."""

import subprocess
from pathlib import Path

import dagster as dg
from dagster import AssetExecutionContext, MaterializeResult

_PROJECT_ROOT = Path(__file__).parent.parent.parent
_TRANSFORM_DIR = _PROJECT_ROOT / "transform"
_DB_PATH = _PROJECT_ROOT / "data" / "meridian.duckdb"
_REPORT_PATH = _TRANSFORM_DIR / "edr_target" / "elementary_report.html"


@dg.asset(
    name="elementary_report",
    group_name="quality",
    description="Elementary data quality HTML report — run after dbt build.",
    deps=["mart_marketplace_daily", "fct_orders"],
)
def elementary_report_asset(context: AssetExecutionContext) -> MaterializeResult:
    result = subprocess.run(
        [
            "uv", "run", "edr", "report",
            "--profiles-dir", ".",
            "--profile-target", "duckdb",
            "--project-dir", ".",
            "--file-path", str(_REPORT_PATH),
        ],
        cwd=_TRANSFORM_DIR,
        capture_output=True,
        text=True,
        env={**__import__("os").environ, "DUCKDB_PATH": str(_DB_PATH)},
    )
    if result.returncode != 0:
        raise RuntimeError(f"edr report failed:\n{result.stderr[-2000:]}")

    report_size = _REPORT_PATH.stat().st_size if _REPORT_PATH.exists() else 0
    context.log.info(f"Elementary report written to {_REPORT_PATH} ({report_size} bytes)")
    return MaterializeResult(
        metadata={
            "report_path": str(_REPORT_PATH),
            "report_size_bytes": report_size,
        }
    )
