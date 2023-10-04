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
    dbt_run_cmd = [DBT_EXE, "run"]
    dbt_run_cmd.extend(["--project-dir", str(project.project_dir)])
    dbt_run_cmd.extend(["--profiles-dir", str(project.profiles_dir)])
    dbt_run_cmd.extend(["-t", profile.target])
    dbt_run_cmd.extend(["-m", model])

    return cmd.run(" ".join(dbt_run_cmd))


def dbt_test(project: DbtProject, profile: DbtProfile, model: str) -> str:
    dbt_test_cmd = [DBT_EXE, "test"]
    dbt_test_cmd.extend(["--project-dir", str(project.project_dir)])
    dbt_test_cmd.extend(["--profiles-dir", str(project.profiles_dir)])
    dbt_test_cmd.extend(["-t", profile.target])
    dbt_test_cmd.extend(["-m", model])

    return cmd.run(" ".join(dbt_test_cmd))
