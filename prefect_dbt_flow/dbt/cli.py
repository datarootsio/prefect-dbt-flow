"""Utility functions for interacting with dbt using command-line commands."""
import shutil
from typing import Optional

from prefect_dbt_flow.dbt import DbtDagOptions, DbtProfile, DbtProject
from prefect_dbt_flow.utils import cmd

DBT_EXE = shutil.which("dbt") or "dbt"


def dbt_ls(
    project: DbtProject,
    dag_options: Optional[DbtDagOptions],
    output: str = "json",
) -> str:
    """
    Code that lists resources from the dbt project, using `dbt ls` command.

    Args:
        project: A class that represents a dbt project configuration.
        dag_options: A class to add dbt DAG configurations.
        output: Format of output, default is JSON.

    Returns:
        list of JSON objects containing dbt resources.
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

    Args:
        project: A class that represents a dbt project configuration.
        profile: A class that represents a dbt profile configuration.
        model: Name of the model to run.

    Returns:
        A string representing the output of the `dbt run` command.
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

    Args:
        project: A class that represents a dbt project configuration.
        profile: A class that represents a dbt profile configuration.
        model: Name of the model to run.

    Returns:
        A string representing the output of the `dbt test` command.
    """
    dbt_test_cmd = [DBT_EXE, "test"]
    dbt_test_cmd.extend(["--project-dir", str(project.project_dir)])
    dbt_test_cmd.extend(["--profiles-dir", str(project.profiles_dir)])
    dbt_test_cmd.extend(["-t", profile.target])
    dbt_test_cmd.extend(["-m", model])

    return cmd.run(" ".join(dbt_test_cmd))
