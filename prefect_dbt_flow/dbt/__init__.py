"""Code for managing and configuring a dbt project."""
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import List, Optional, Union


class DbtResourceType(Enum):
    """
    Enum class that represents a dbt resource type.
    """

    MODEL = auto()
    SEED = auto()
    SNAPSHOT = auto()


@dataclass
class DbtProject:
    """
    Class that represents a dbt project configuration.

    Args:
        name: Name of dbt project,
        project_dir: Path to directory that contains dbt project.yml
        profiles_dir: Path to directory that contains dbt profiles.yml
    """

    name: str
    project_dir: Union[str, Path]
    profiles_dir: Union[str, Path]


@dataclass
class DbtProfile:
    """
    Class that represents a dbt profile configuration.

    Args:
        target: dbt target, usualy "dev" or "prod"
        overrides: dbt profile overrides
    """

    target: str
    overrides: Optional[dict[str, str]] = None


@dataclass
class DbtNode:
    """
    Class that represents a dbt node in the project.

    Args:
        name: dbt node name, e. my_model_a
        unique_id: dbt id e. model.sample_project.my_model_a
        resource_type: dbt resource type, e. model or seed
        depends_on: e. ["model.sample_project.my_model_b"]
        has_tests: if node is a test
    """

    name: str
    unique_id: str
    resource_type: DbtResourceType
    depends_on: List[str]
    has_tests: bool = False


@dataclass
class DbtDagOptions:
    """
    Class to add dbt DAG configurations.

    Args:
        select: dbt module to include in the run
        exclude: dbt module to exclude in the run
        run_test_after_model: run test afeter run model
        vars: dbt vars
        install_deps: install dbt dependencies, default behavior install deps
    """

    select: Optional[str] = None
    exclude: Optional[str] = None
    run_test_after_model: bool = False
    vars: Optional[dict[str, str]] = None
    install_deps: bool = True
