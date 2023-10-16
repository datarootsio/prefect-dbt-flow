# Dev env

Temporary dev env for testing.

TODO: simplify this

## docker-compose

Run following commands in root of this repo. (not in .dev)

```bash
docker compose --file .dev/docker-compose.yml up --build -d
docker compose --file .dev/docker-compose.yml down

# To easily connect to service in the dev env use the following command
# will mount an example in the container
docker compose --file .dev/docker-compose.yml run cli
```

```bash
# to deploy run command in prefect cli container:
docker compose --file .dev/docker-compose.yml run cli

prefect deployment build \
    -sb "remote-file-system/prefect-flows" \
    -n "dbt-test" \
    -q "default" \
    -p "default-agent-pool" \
    -a \
    "dbt_flow.py:run_dbt"
```

## Testing from "outside" docker-compose

```bash
cd ./examples/sample_project
poetry run dbt run -t test
poetry run python my_dbt_flow.py
```

## Deploy prefect flow

```bash
# dbt_flow.py
prefect deployment build \
    -sb "remote-file-system/prefect-flows" \
    -n "dbt-test" \
    -q "default" \
    -p "default-agent-pool" \
    -a \
    "dbt_flow.py:run_dbt"
```

## DBT database backend

pgadmin: localhost:8080
un: admin@admin.admin; pw: admin

create db connection from pgadmin
name: db
connection: db
username: admin
password: admin

## Minio: prefect Storage backend

minio: localhost:9000
un: minioadmin; pw: minioadmin
create bucket: prefect-flows
create and access token => you get <minio-key> and <minio-secret>

## Prefect

prefect: localhost:4200
create RemoteFileSystem block
Basepath
s3://prefect-flows/flows
Settings
{
  "key": "<minio-key>",
  "secret": "<minio-secret>",
  "client_kwargs": {
    "endpoint_url": "http://minio:9000"
  }
}
