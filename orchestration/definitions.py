"""Top-level Dagster Definitions for the Meridian batch data platform."""

from __future__ import annotations

import dagster as dg
from dagster_dlt import DagsterDltResource

from orchestration.assets.ingest import meridian_dlt_assets

defs = dg.Definitions(
    assets=[meridian_dlt_assets],
    resources={
        "dlt": DagsterDltResource(),
    },
)
