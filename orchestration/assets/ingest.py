"""Dagster dlt assets — wrap the meridian dlt pipeline as software-defined assets."""

from dagster import AssetExecutionContext
from dagster_dlt import DagsterDltResource, dlt_assets

from ingestion.meridian_source import meridian_source
from ingestion.pipeline import build_pipeline


@dlt_assets(
    dlt_source=meridian_source(),
    dlt_pipeline=build_pipeline(),
    name="meridian_raw",
    group_name="raw",
)
def meridian_dlt_assets(
    context: AssetExecutionContext,
    dlt: DagsterDltResource,
) -> object:
    yield from dlt.run(context=context)
