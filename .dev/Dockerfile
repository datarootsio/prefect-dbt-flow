FROM prefecthq/prefect:2.10.17-python3.11

COPY ./.dev/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY prefect_dbt_flow/ prefect_dbt_flow/
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
COPY README.md README.md

RUN poetry config virtualenvs.create false --local

RUN poetry install --no-dev
