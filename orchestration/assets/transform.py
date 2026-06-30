"""Dagster dbt assets — wraps the meridian_batch dbt project as software-defined assets."""

from pathlib import Path

import dagster as dg
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets

TRANSFORM_DIR = Path(__file__).parent.parent.parent / "transform"

dbt_project = DbtProject(
    project_dir=TRANSFORM_DIR,
    profiles_dir=TRANSFORM_DIR,
)


@dbt_assets(
    manifest=dbt_project.manifest_path,
    name="meridian_dbt",
    dagster_dbt_translator=None,
)
def meridian_dbt_assets(
    context: dg.AssetExecutionContext,
    dbt: DbtCliResource,
) -> object:
    yield from dbt.cli(["build", "--profiles-dir", str(TRANSFORM_DIR)], context=context).stream()
