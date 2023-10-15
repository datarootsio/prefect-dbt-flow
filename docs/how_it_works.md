# How it works
Here, we briefly explain how prefect-dbt-flow works under the hood.

1. Based on the configuration provided by the user, we look for the dbt project directory and using the `dbt ls` command (which returns a json structure) we try to parse all the "dbt nodes". The dbt nodes we are interested in are the model/tests/seed and snapshot nodes. The `dbt ls` command also provides us with the dbt DAG. Each node defines its upstream dependencies.
2. For each dbt node we create a Prefect task, meaning that each Prefect tasks executes one single model/test/seed/snapshot.
3. Based on the dbt node dependencies we set the dependencies between the Prefect tasks.
4. Lastly we wrap all the Prefect tasks in a Prefect flow and return it to the user.

If you want a more detailed explanation we would recommend you to read the source code of the source code.