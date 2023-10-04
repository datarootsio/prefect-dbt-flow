"""Utility functions for interacting with dbt using command-line commands."""
from typing import Optional
import shutil

from prefect_dbt_flow.dbt import DbtProject, DbtProfile, DbtDagOptions
from prefect_dbt_flow.utils import cmd


DBT_EXE = shutil.which("dbt") or "dbt"


def dbt_ls(
    project: DbtProject,
    dag_options: Optional[DbtDagOptions],
    output: str = "json",
) -> str:
    """
    Code that lists resources from the dbt project, using `dbt ls` command.

    :param project: Class that represents a dbt project configuration.
    :param dag_otpions: Class to add dbt DAG configurations.
    :param output: Controls the format of output, default is JSON.
    :return: list of JSON objects containing dbt resources.
    """
    dbt_ls_cmd = [DBT_EXE, "ls"]
    dbt_ls_cmd.extend(["--project-dir", str(project.project_dir)])
    dbt_ls_cmd.extend(["--profiles-dir", str(project.profiles_dir)])
    dbt_ls_cmd.extend(["--output", output])

    if dag_options:
        if dag_options.select:
            dbt_ls_cmd.extend(["--select", dag_options.select])
        if dag_options.exclude:
            dbt_ls_cmd.extend(["--exclude", dag_options.exclude])

    return cmd.run(" ".join(dbt_ls_cmd))


def dbt_run(project: DbtProject, profile: DbtProfile, model: str) -> str:
    """
    Function that executes `dbt run` command

    :param project: Class that represents a dbt project configuration.
    :param profile: Class that represents a dbt profile configuration.
    :param model: Name of the model to run.
    :return: string representing the output of the `dbt run` command.
    """
    dbt_run_cmd = [DBT_EXE, "run"]
    dbt_run_cmd.extend(["--project-dir", str(project.project_dir)])
    dbt_run_cmd.extend(["--profiles-dir", str(project.profiles_dir)])
    dbt_run_cmd.extend(["-t", profile.target])
    dbt_run_cmd.extend(["-m", model])

    return cmd.run(" ".join(dbt_run_cmd))


def dbt_test(project: DbtProject, profile: DbtProfile, model: str) -> str:
    """
    Function that executes `dbt test` command
    
    :param project: Class that represents a dbt project configuration.
    :param profile: Class that represents a dbt profile configuration.
    :param model: Name of the model to run.
    :return: string representing the output of the `dbt test` command.
    """
    dbt_test_cmd = [DBT_EXE, "test"]
    dbt_test_cmd.extend(["--project-dir", str(project.project_dir)])
    dbt_test_cmd.extend(["--profiles-dir", str(project.profiles_dir)])
    dbt_test_cmd.extend(["-t", profile.target])
    dbt_test_cmd.extend(["-m", model])

    return cmd.run(" ".join(dbt_test_cmd))
