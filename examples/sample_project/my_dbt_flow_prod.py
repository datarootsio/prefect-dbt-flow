from pathlib import Path

from prefect.task_runners import SequentialTaskRunner

from prefect_dbt_flow.dbt import DbtProject, DbtProfile
from prefect_dbt_flow import dbt_flow

my_dbt_flow = dbt_flow(
    project=DbtProject(
        name="sample_project",
        project_dir=Path(__file__).parent,
        profiles_dir=Path(__file__).parent,
    ),
    profile=DbtProfile(
        target="prod",
    ),
    flow_kwargs={
        # Ensure only one process has access to the duckdb database file at the same time
        "task_runner": SequentialTaskRunner(),
    },
)

if __name__ == "__main__":
    my_dbt_flow()
