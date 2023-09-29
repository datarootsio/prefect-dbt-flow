from typing import List, Dict, Optional

from prefect import task
from prefect_dbt_flow_2.utils import DbtConfig, DbtNode

# from prefect_dbt_flow.dbt import DbtNode, _run_cmd
# from prefect_dbt_flow import cmd

DBT_RUN_EMOJI = "🏃"
DBT_TEST_EMOJI = "🧪"


def _task_dbt_run(dbt_node: DbtNode, task_kwargs: Optional[Dict] = None):
    all_task_kwargs = {
        **(task_kwargs or {}),
        "name": f"{DBT_RUN_EMOJI} {dbt_node.name}",
    }

    @task(**all_task_kwargs)
    def dbt_run():
        dbt_run_command = [ #what about the other options of dbt run ?
            DBT_EXE, #need to provide this
            "run",
            "-t",
            "dev", #this should be and option [dev | prod]
            "--project-dir",
            str(DBT_PROJECT_DIR.absolute()), #need to provide this env?
            "--profiles-dir",
            str(DBT_PROJECT_DIR.absolute()), #neet to provide this env?
            "-m",
            dbt_node.name,
        ]
        _run_cmd(dbt_run_command)

    return dbt_run


def _task_dbt_test(dbt_node: DbtNode, task_kwargs: Optional[Dict] = None):
    all_task_kwargs = {
        **(task_kwargs or {}),
        "name": f"{DBT_TEST_EMOJI} {dbt_node.name}",
    }

    @task(**all_task_kwargs)
    def dbt_test():
        dbt_run_command = [ #what about the other options of dbt test?
            DBT_EXE, #need to provide this
            "test",
            "-t",
            "dev", #this should be and option [dev | prod]
            "--project-dir",
            str(DBT_PROJECT_DIR.absolute()), #need to provide this env?
            "--profiles-dir",
            str(DBT_PROJECT_DIR.absolute()), #neet to provide this env?
            "-m",
            dbt_node.name,
        ]
        _run_cmd(dbt_run_command)
    

    return dbt_test


def generate_tasks_dag(
    dbt_graph: List[DbtNode],
    dbt_config=DbtConfig,
):
    dbt_tasks_dag = list()

    if dbt_config.dbt_run_test_after_model:
        for node in dbt_graph:
            node.name
            node.resource_type
            node.depends_on

            dbt_config.dbt_target
            dbt_config.dbt_project_dir
            dbt_config.dbt_project_dir
            dbt_config.dbt_run_test_after_model
            _task_dbt_test()

    else:
        for node in dbt_graph:
            node.name
            node.resource_type
            node.depends_on

            dbt_config.dbt_target
            dbt_config.dbt_project_dir
            dbt_config.dbt_project_dir
            dbt_config.dbt_run_test_after_model
            _task_dbt_run()
    

    
    return dbt_tasks_dag