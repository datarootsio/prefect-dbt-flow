from pathlib import Path

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
)

if __name__ == "__main__":
    my_dbt_flow()
