from typing import List, Dict, Optional

from prefect import task
from utils import DbtConfig, DbtNode, cmd, logging_config

logger = logging_config.logger

DBT_RUN_EMOJI = "🏃"
DBT_TEST_EMOJI = "🧪"


def _task_dbt_run(dbt_node: DbtNode,
                   dbt_config: DbtConfig,
                   task_kwargs: Optional[Dict] = None):
    all_task_kwargs = {
        **(task_kwargs or {}),
        "name": f"{DBT_TEST_EMOJI} {dbt_node.name}",
        #"description": "task description",
        #"tags":["?"],
        #"retries": 1,
        #"retry_delay_seconds":, 5,
        #"log_prints": False,
        #"persist_result":False,
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
        cmd._run_cmd(dbt_run_command)
        
    dbt_run()
    return dbt_run


def _task_dbt_test(dbt_node: DbtNode,
                   dbt_config: DbtConfig,
                   name:str,
                   wait_for,
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
        cmd._run_cmd(dbt_run_command)
    
    dbt_test()
    return dbt_test
