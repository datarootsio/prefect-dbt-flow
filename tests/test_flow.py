import shutil
from contextlib import contextmanager
from pathlib import Path

import duckdb
import pytest
from prefect.task_runners import ThreadPoolTaskRunner
from prefect.testing.utilities import prefect_test_harness

from prefect_dbt_flow import dbt_flow
from prefect_dbt_flow.dbt import DbtDagOptions, DbtProfile, DbtProject

SAMPLE_PROJECT_PATH = Path(__file__).parent.parent / "examples" / "sample_project"
JAFFLE_SHOP_PATH = Path(__file__).parent.parent / "examples" / "jaffle_shop_duckdb"


@pytest.fixture(autouse=True, scope="session")
def prefect_test_fixture():
    with prefect_test_harness():
        yield


@pytest.fixture
def duckdb_db_file(monkeypatch, tmp_path: Path):
    duckdb_db_file = tmp_path / "dbt_test.duckdb"
    monkeypatch.setenv("DUCKDB_DB_FILE", str(duckdb_db_file))

    yield duckdb_db_file


@contextmanager
def dbt_package(project_path: Path, content: str):
    package_yaml_path = project_path / "packages.yml"
    dbt_packages_path = project_path / "dbt_packages"

    package_yaml_path.write_text(content)

    try:
        yield
    finally:
        shutil.rmtree(str(dbt_packages_path.absolute()))
        package_yaml_path.unlink(missing_ok=True)


def test_flow_sample_project(duckdb_db_file: Path):
    dbt_project_path = SAMPLE_PROJECT_PATH

    my_dbt_flow = dbt_flow(
        project=DbtProject(
            name="sample_project",
            project_dir=dbt_project_path,
            profiles_dir=dbt_project_path,
        ),
        profile=DbtProfile(
            target="test",
        ),
        flow_kwargs={
            # Ensure only one process has access to the duckdb db
            # file at the same time
            "task_runner": ThreadPoolTaskRunner(max_workers=1),
        },
    )

    my_dbt_flow()

    with duckdb.connect(str(duckdb_db_file)) as ddb:
        assert len(ddb.sql("SHOW ALL TABLES").fetchall()) == 4
        assert ddb.sql("SELECT * FROM my_model_d ORDER BY id").fetchall() == [
            (1,),
            (2,),
            (3,),
            (4,),
        ]


def test_flow_sample_project_with_tests(duckdb_db_file: Path):
    dbt_project_path = SAMPLE_PROJECT_PATH

    my_dbt_flow = dbt_flow(
        project=DbtProject(
            name="sample_project",
            project_dir=dbt_project_path,
            profiles_dir=dbt_project_path,
        ),
        profile=DbtProfile(
            target="test",
        ),
        dag_options=DbtDagOptions(
            run_test_after_model=True,
        ),
        flow_kwargs={
            # Ensure only one process has access to the duckdb db
            # file at the same time
            "task_runner": ThreadPoolTaskRunner(max_workers=1),
        },
    )

    my_dbt_flow()

    with duckdb.connect(str(duckdb_db_file)) as ddb:
        assert len(ddb.sql("SHOW ALL TABLES").fetchall()) == 4
        assert ddb.sql("SELECT * FROM my_model_d ORDER BY id").fetchall() == [
            (1,),
            (2,),
            (3,),
            (4,),
        ]


def test_flow_sample_project_select(duckdb_db_file: Path):
    dbt_project_path = SAMPLE_PROJECT_PATH

    my_dbt_flow = dbt_flow(
        project=DbtProject(
            name="sample_project",
            project_dir=dbt_project_path,
            profiles_dir=dbt_project_path,
        ),
        profile=DbtProfile(
            target="test",
        ),
        dag_options=DbtDagOptions(
            select="+my_model_c",
        ),
        flow_kwargs={
            # Ensure only one process has access to the duckdb db
            # file at the same time
            "task_runner": ThreadPoolTaskRunner(max_workers=1),
        },
    )

    my_dbt_flow()

    with duckdb.connect(str(duckdb_db_file)) as ddb:
        assert len(ddb.sql("SHOW ALL TABLES").fetchall()) == 3


def test_flow_sample_project_exclude(duckdb_db_file: Path):
    dbt_project_path = SAMPLE_PROJECT_PATH

    my_dbt_flow = dbt_flow(
        project=DbtProject(
            name="sample_project",
            project_dir=dbt_project_path,
            profiles_dir=dbt_project_path,
        ),
        profile=DbtProfile(
            target="test",
        ),
        dag_options=DbtDagOptions(
            exclude="my_model_c+",
        ),
        flow_kwargs={
            # Ensure only one process has access to the duckdb db
            # file at the same time
            "task_runner": ThreadPoolTaskRunner(max_workers=1),
        },
    )

    my_dbt_flow()

    with duckdb.connect(str(duckdb_db_file)) as ddb:
        assert len(ddb.sql("SHOW ALL TABLES").fetchall()) == 2


def test_flow_jaffle_shop(duckdb_db_file: Path):
    dbt_project_path = JAFFLE_SHOP_PATH

    my_dbt_flow = dbt_flow(
        project=DbtProject(
            name="jaffle_shop",
            project_dir=dbt_project_path,
            profiles_dir=dbt_project_path,
        ),
        profile=DbtProfile(
            target="test",
        ),
        flow_kwargs={
            # Ensure only one process has access to the duckdb db
            # file at the same time
            "task_runner": ThreadPoolTaskRunner(max_workers=1),
        },
    )

    my_dbt_flow()

    with duckdb.connect(str(duckdb_db_file)) as ddb:
        assert len(ddb.sql("SHOW ALL TABLES").fetchall()) == 9


def test_flow_sample_project_overrides_new_profile(duckdb_db_file: Path):
    dbt_project_path = SAMPLE_PROJECT_PATH

    my_dbt_flow = dbt_flow(
        project=DbtProject(
            name="sample_project",
            project_dir=dbt_project_path,
            profiles_dir=dbt_project_path,
        ),
        profile=DbtProfile(
            target="something_else",
            overrides={
                "type": "duckdb",
                "path": str(duckdb_db_file.absolute()),
            },
        ),
        flow_kwargs={
            # Ensure only one process has access to the duckdb db
            # file at the same time
            "task_runner": ThreadPoolTaskRunner(max_workers=1),
        },
    )

    my_dbt_flow()

    with duckdb.connect(str(duckdb_db_file)) as ddb:
        assert len(ddb.sql("SHOW ALL TABLES").fetchall()) == 4


def test_flow_sample_project_overrides_existing_profile(duckdb_db_file: Path):
    dbt_project_path = SAMPLE_PROJECT_PATH

    my_dbt_flow = dbt_flow(
        project=DbtProject(
            name="sample_project",
            project_dir=dbt_project_path,
            profiles_dir=dbt_project_path,
        ),
        profile=DbtProfile(
            target="override_in_test",
            overrides={
                "path": str(duckdb_db_file.absolute()),
            },
        ),
        flow_kwargs={
            # Ensure only one process has access to the duckdb db
            # file at the same time
            "task_runner": ThreadPoolTaskRunner(max_workers=1),
        },
    )

    my_dbt_flow()

    with duckdb.connect(str(duckdb_db_file)) as ddb:
        assert len(ddb.sql("SHOW ALL TABLES").fetchall()) == 4


def test_flow_sample_project_dont_specify_target(duckdb_db_file: Path):
    dbt_project_path = SAMPLE_PROJECT_PATH

    my_dbt_flow = dbt_flow(
        project=DbtProject(
            name="sample_project",
            project_dir=dbt_project_path,
            profiles_dir=dbt_project_path,
        ),
        flow_kwargs={
            # Ensure only one process has access to the duckdb db
            # file at the same time
            "task_runner": ThreadPoolTaskRunner(max_workers=1),
        },
    )

    my_dbt_flow()

    with duckdb.connect(str(duckdb_db_file)) as ddb:
        assert len(ddb.sql("SHOW ALL TABLES").fetchall()) == 4


def test_flow_sample_project_vars(duckdb_db_file: Path):
    dbt_project_path = SAMPLE_PROJECT_PATH

    my_dbt_flow = dbt_flow(
        project=DbtProject(
            name="sample_project",
            project_dir=dbt_project_path,
            profiles_dir=dbt_project_path,
        ),
        profile=DbtProfile(
            target="vars_test",
        ),
        dag_options=DbtDagOptions(
            vars={
                "adapter_type": "duckdb",
                "duckdb_db_path": str(duckdb_db_file.absolute()),
            },
        ),
        flow_kwargs={
            # Ensure only one process has access to the duckdb db
            # file at the same time
            "task_runner": ThreadPoolTaskRunner(max_workers=1),
        },
    )

    my_dbt_flow()

    with duckdb.connect(str(duckdb_db_file)) as ddb:
        assert len(ddb.sql("SHOW ALL TABLES").fetchall()) == 4


def test_flow_sample_project_install_deps(duckdb_db_file: Path):
    dbt_project_path = SAMPLE_PROJECT_PATH
    packages_yml_content = (
        """packages:\n"""
        """  - package: dbt-labs/dbt_utils\n"""
        """    version: "{{ var('dbt_utils_version') }}"\n"""
    )

    my_dbt_flow = dbt_flow(
        project=DbtProject(
            name="sample_project",
            project_dir=dbt_project_path,
            profiles_dir=dbt_project_path,
        ),
        dag_options=DbtDagOptions(
            vars={
                "dbt_utils_version": "1.1.1",
            },
            install_deps=True,
        ),
        flow_kwargs={
            # Ensure only one process has access to the duckdb db
            # file at the same time
            "task_runner": ThreadPoolTaskRunner(max_workers=1),
        },
    )

    with dbt_package(dbt_project_path, content=packages_yml_content):
        my_dbt_flow()

    with duckdb.connect(str(duckdb_db_file)) as ddb:
        assert len(ddb.sql("SHOW ALL TABLES").fetchall()) == 4
