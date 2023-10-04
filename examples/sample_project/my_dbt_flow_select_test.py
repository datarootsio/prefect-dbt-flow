from pathlib import Path

from prefect_dbt_flow.dbt import DbtProject, DbtProfile, DbtDagOptions
from prefect_dbt_flow import dbt_flow

my_dbt_flow = dbt_flow(
    project=DbtProject(
        name="sample_project",
        project_dir=Path(__file__).parent,
        profiles_dir=Path(__file__).parent,
    ),
    profile=DbtProfile(
        target="test",
    ),
    dag_options=DbtDagOptions(
        select="+my_model_c",
        run_test_after_model=True,
    ),
)

if __name__ == "__main__":
    my_dbt_flow()
