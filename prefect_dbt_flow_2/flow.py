import shutil
from utils import flow, logging_config


logger = logging_config.logger

if __name__ == "__main__":

    logger.debug("--- Start run")
    flow.dbt_flow(
        dbt_project_name="prefect_dbt",
        dbt_project_dir="/Users/dvaldez/DataRoots/guilds/prefect-dbt-backup/prefect_dbt",
        dbt_profiles_dir="/Users/dvaldez/DataRoots/guilds/prefect-dbt-backup/prefect_dbt",
        dbt_target="dev",
        dbt_exe= shutil.which("dbt"),
        dbt_run_test_after_model=True,
        dbt_print_stauts=False,
        flow_kwargs= {"name":"xxx"}
    )

    logger.debug("--- End run")