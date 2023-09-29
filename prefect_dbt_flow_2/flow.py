from prefect_dbt_flow_2.utils.flow import dbt_flow

dev_flow = dbt_flow(
    dbt_project_name="project_name",
    dbt_project_dir="path/to/dbt/project",
    dbt_profiles_dir="path/to/dbt_profiles",
    dbt_target="dev",
    dbt_run_test_after_model=True,
    dbt_print_stauts=True,
    flow_kwargs= {"name":"xxx1"}
)

prod_flow = dbt_flow(
    dbt_project_name="project_name",
    dbt_project_dir="path/to/dbt/project",
    dbt_profiles_dir="path/to/dbt_profiles",
    dbt_target="prod",
    dbt_run_test_after_model=True,
    dbt_print_stauts=True,
    flow_kwargs= {"name":"xxx2"}
)

if __name__ == "__main__":
    print(dev_flow)
    print(prod_flow)
