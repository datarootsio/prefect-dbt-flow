from pathlib import Path

from prefect_dbt_flow import dbt_flow
from prefect_dbt_flow.dbt import DbtDagOptions, DbtProfile, DbtProject

my_dbt_flow = dbt_flow(
    project=DbtProject(
        name="example_jaffle_shop",
        project_dir=Path(__file__).parent,
        profiles_dir=Path(__file__).parent,
    ),
    profile=DbtProfile(
        target="dev",
    ),
    dag_options=DbtDagOptions(
        run_test_after_model=True,
    ),
)

if __name__ == "__main__":
    my_dbt_flow()
