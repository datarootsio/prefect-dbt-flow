from prefect_dbt_flow.flow import dbt_flow
from prefect_dbt_flow.dbt import DbtProject, DbtProfile
import os

dbt_project = DbtProject(
    name="project_name",
    project_dir=os.getcwd()
)
dbt_profile = DbtProfile(
    name="project_name",
    project_dir=os.getcwd()
)

run = dbt_flow(
    project=dbt_project,
    profile = dbt_profile,
    run_test_after_model=True,
    flow_kwargs={
        "target":"dev" #what if you want to change the dbt target ?
    }
)