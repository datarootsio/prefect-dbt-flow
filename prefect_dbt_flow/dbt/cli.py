import shutil

from prefect_dbt_flow.dbt import DbtProject, DbtProfile
from prefect_dbt_flow.utils import cmd


DBT_EXE = shutil.which("dbt") or "dbt"


def dbt_ls(project: DbtProject, output: str = "json") -> str:
    dbt_ls_cmd = [DBT_EXE, "ls"]
    dbt_ls_cmd.extend(["--project-dir", project.project_dir])
    dbt_ls_cmd.extend(["--profiles-dir", project.profiles_dir])
    dbt_ls_cmd.extend(["--output", output])

    return cmd.run(" ".join(dbt_ls_cmd))


def dbt_run(project: DbtProject, profile: DbtProfile, models: str) -> str:
    dbt_run_cmd = [DBT_EXE, "run"]
    dbt_run_cmd.extend(["--project-dir", project.project_dir])
    dbt_run_cmd.extend(["--profiles-dir", project.profiles_dir])
    dbt_run_cmd.extend(["-t", profile.target])
    dbt_run_cmd.extend(["-m", models])

    return cmd.run(" ".join(dbt_run_cmd))


def dbt_test(project: DbtProject, profile: DbtProfile, models: str) -> str:
    dbt_test_cmd = [DBT_EXE, "test"]
    dbt_test_cmd.extend(["--project-dir", project.project_dir])
    dbt_test_cmd.extend(["--profiles-dir", project.profiles_dir])
    dbt_test_cmd.extend(["-t", profile.target])
    dbt_test_cmd.extend(["-m", models])

    return cmd.run(" ".join(dbt_test_cmd))
