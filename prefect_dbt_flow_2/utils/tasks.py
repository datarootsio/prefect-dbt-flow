from typing import List, Dict, Optional

from prefect import task
from prefect_dbt.cli.commands import trigger_dbt_cli_command
from prefect_dbt_flow_2.utils import DbtConfig, DbtNode
from prefect_dbt_flow_2.utils.cmd import _run_cmd

DBT_RUN_EMOJI = "🏃"
DBT_TEST_EMOJI = "🧪"


def _task_dbt_run(dbt_node: DbtNode,
                   dbt_config: DbtConfig,
                   task_kwargs: Optional[Dict] = None):
    all_task_kwargs = {
        **(task_kwargs or {}),
        "name": f"{DBT_TEST_EMOJI} {dbt_node.name}",
    }

    @task(**all_task_kwargs)
    def dbt_run():
        dbt_run_command = [ #what about the other options of dbt run ?
            dbt_config.dbt_exe, #need to provide this
            "run",
            "-t",
            dbt_config.dbt_target, #this should be and option [dev | prod]
            "--project-dir",
            dbt_config.dbt_project_dir, #need to provide this env?
            "--profiles-dir",
            dbt_config.dbt_profiles_dir, #neet to provide this env?
            "-m",
            dbt_node.name,
        ]
        _run_cmd(dbt_run_command)

    return dbt_run


def _task_dbt_test(dbt_node: DbtNode,
                   dbt_config: DbtConfig,
                   task_kwargs: Optional[Dict] = None):
    all_task_kwargs = {
        **(task_kwargs or {}),
        "name": f"{DBT_TEST_EMOJI} {dbt_node.name}",
    }

    @task(**all_task_kwargs)
    def dbt_test():
        dbt_run_command = [ #what about the other options of dbt test?
            dbt_config.dbt_exe, #need to provide this
            "test",
            "-t",
            dbt_config.dbt_target, #this should be and option [dev | prod]
            "--project-dir",
            dbt_config.dbt_project_dir, #need to provide this env?
            "--profiles-dir",
            dbt_config.dbt_profiles_dir, #neet to provide this env?
            "-m",
            dbt_node.name,
        ]
        _run_cmd(dbt_run_command)


    return dbt_test

def geneate_tasks_dag(dbt_graph: list(DbtNode), dbt_config: DbtConfig):
    for dbt_node in dbt_graph:
        if dbt_config.dbt_run_test_after_model:
            future_run = trigger_dbt_cli_command.with_options( #will create a prefect future
                name=dbt_node.name,
                # retries="", #Do we need this? it goes in dbt_config of prefect config?
                # retry_delay_seconds="",
            ).submint(
                _task_dbt_run,
                project_dir=dbt_config.dbt_project_dir,
                dbt_cli_profile=dbt_config.dbt_profiles_dir,
                overwrite_profiles=True, #Why do we do this?
                wait_for=dbt_node.depends_on
            )
            state_run = future_run.wait()

            future_test = trigger_dbt_cli_command.with_options( #will create a prefect future
                name=dbt_node.name,
                # retries="", #Do we need this? it goes in dbt_config of prefect config?
                # retry_delay_seconds="",
            ).submint(
                _task_dbt_test,
                project_dir=dbt_config.dbt_project_dir,
                dbt_cli_profile=dbt_config.dbt_profiles_dir,
                overwrite_profiles=True, #Why do we do this?
                wait_for=[future_run, dbt_node.depends_on]
            )
            state_test = future_test.wait()

            return future_test
        else:
            future_run = trigger_dbt_cli_command.with_options( #will create a prefect future
                name=dbt_node.name,
                # retries="", #Do we need this? it goes in dbt_config of prefect config?
                # retry_delay_seconds="",
            ).submint(
                _task_dbt_run,
                project_dir=dbt_config.dbt_project_dir,
                dbt_cli_profile=dbt_config.dbt_profiles_dir,
                overwrite_profiles=True, #Why do we do this?
                wait_for=dbt_node.depends_on
            )
            state_run = future_run.wait()

            return future_run

