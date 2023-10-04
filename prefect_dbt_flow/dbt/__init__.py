from typing import List, Union, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DbtProject:
    name: str
    project_dir: Union[str, Path]
    profiles_dir: Union[str, Path]


@dataclass
class DbtProfile:
    target: str


@dataclass
class DbtNode:
    name: str
    unique_id: str
    resource_type: str
    depends_on: List[str]
    has_tests: bool = False


@dataclass
class DbtDagOptions:
    select: Optional[str] = None
    exclude: Optional[str] = None
    run_test_after_model: bool = False
