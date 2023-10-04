"""Code for managing and configuring a dbt project."""
from typing import List, Union, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DbtProject:
    """
    Class that represents a dbt project configuration.

    :field name: Name of dbt project,
    :field project_dir: Path to directory that contains dbt project.yml
    :field profiles_dir: Path to directory that contains dbt profiles.yml
    """

    name: str
    project_dir: Union[str, Path]
    profiles_dir: Union[str, Path]


@dataclass
class DbtProfile:
    """
    Class that represents a dbt profile configuration.

    :field target: dbt target, usualy "dev" or "prod"
    """

    target: str


@dataclass
class DbtNode:
    """
    Class that represents a dbt node in the project.

    :field name: dbt node name, e. my_model_a
    :field unique_id: dbt id e. model.sample_project.my_model_a
    :field resource_type: "model" or "test"
    :field depends_on: e. ["model.sample_project.my_model_b"]
    :field has_tests: if node is a test
    """

    name: str
    unique_id: str
    resource_type: str
    depends_on: List[str]
    has_tests: bool = False


@dataclass
class DbtDagOptions:
    """
    Class to add dbt DAG configurations.

    :field select: dbt module to include in the run
    :field exclude: dbt module to exclude in the run
    :field run_test_after_model: run test afeter run model
    """

    select: Optional[str] = None
    exclude: Optional[str] = None
    run_test_after_model: bool = False
