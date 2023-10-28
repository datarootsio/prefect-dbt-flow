# Profile overrides

When using dbt, you might want to dynamically change the profile configuration based for example on the environment you are running in. Also some profile configurations might be sensitive and you might not want to store them in your repository. Profile overrides allow you to inject profile configurations via python code, at runtime. In this section we will show you how to use profile overrides.

## Basic usage

To override a profile you must past the `DbtProfile` dataclass to the dbt_flow function.

Profile overrides handle the following cases:

 - When a `profile.yml` is detected in the configured `profiles_dir` it will read in the profile and override the values with the values in the `overrides` dict. The values that are not overridden will be kept as is.
 - When no `profile.yml` is detected it will create a new `profile.yml` with the values in the `overrides` dict. In this case you need to provide all the values needed for your dbt adapter.

## Example


Contents of `path_to/jaffle_shop/profile.yml` BEFORE override:
```yaml
example_jaffle_shop:
  target: dev
  outputs:
    dev:
      type: postgres
      host: data-db
      port: 5432
      dbname: data
```

Configuring the profile overrides:
```python
import os

from prefect import variables
from prefect.blocks.system import Secret

postgres_user = variables.get("POSTGRES_USER")
postgres_pw = Secret.load("POSTGRES_PASSWORD").get()

my_flow = dbt_flow(
    project=DbtProject(
        ...,
        profiles_dir="path_to/jaffle_shop",
    ),
    profile=DbtProfile(
        target="dev",
        overrides={
            "user": postgres_user,
            "password": postgres_pw,
            "schema": os.environ["POSTGRES_SCHEMA"],
            "connect_timeout": 30,
        },
    ),
)
```

Contents of `path_to/jaffle_shop/profile.yml` AFTER override:
```yaml
example_jaffle_shop:
  target: dev
  outputs:
    dev:
      type: postgres
      host: data-db
      port: 5432
      dbname: data
      user: admin
      password: super-secret-password
      schema: example
      connect_timeout: 30
```
