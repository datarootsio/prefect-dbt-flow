"""Logic to override dbt profiles.yml"""
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Generator, Optional

import yaml  # type: ignore

from prefect_dbt_flow.dbt import DbtProfile, DbtProject


@contextmanager
def override_profile(
    project: DbtProject, profile: Optional[DbtProfile]
) -> Generator[DbtProject, None, None]:
    """
    Override dbt profiles.yml with the given profile configuration.

    Args:
        project: A class that represents a dbt project configuration.
        profile: A class that represents a dbt profile configuration.

    Returns:
        dbt_project: DbtProject.
    """
    if not profile or not profile.overrides:
        yield project
        return

    dbt_project_name = _get_dbt_project_name(Path(project.project_dir))
    dbt_profile_path = Path(project.profiles_dir) / "profiles.yml"

    existing_profile_content = {}

    if dbt_profile_path.exists():
        existing_profile_content = (
            yaml.safe_load(dbt_profile_path.read_text())
            .get(dbt_project_name, {})
            .get("outputs", {})
            .get(profile.target, {})
        )

    with TemporaryDirectory() as tmp_profiles_dir:
        tmp_profiles_path = Path(tmp_profiles_dir) / "profiles.yml"
        with open(tmp_profiles_path, "w") as tmp_profiles_file:
            yaml.safe_dump(
                {
                    dbt_project_name: {
                        "target": profile.target,
                        "outputs": {
                            profile.target: {
                                **existing_profile_content,
                                **profile.overrides,
                            }
                        },
                    },
                },
                tmp_profiles_file,
            )

        yield DbtProject(
            name=project.name,
            project_dir=project.project_dir,
            profiles_dir=tmp_profiles_dir,
        )


def _get_dbt_project_name(project_dir: Path) -> str:
    dbt_project_path = project_dir / "dbt_project.yml"

    if not dbt_project_path.exists():
        raise ValueError(f"dbt_project.yml not found in {project_dir}")

    with open(dbt_project_path) as f:
        return yaml.safe_load(f)["name"]
