# Getting started guide

The Prefect-dbt-flow library allows you to seamlessly integrate dbt workflows into Prefect. This usage guide will walk you through the steps required to create and manage a Prefect flow for your dbt project.

## Example guide
This guide will walk you through setting up and running a sample Prefect-dbt-flow using Docker Compose. Follow these steps to get started:

### 1. Clone this repository
Clone the Prefect-dbt-flow repository and navigate to the example directory.
```bash
git clone git@github.com:datarootsio/prefect-dbt-flow.git
cd prefect-dbt-flow/example/jaffle_shop
```

### 2. Install Docker Compose
Ensure that you have Docker Compose installed on your system. If you haven't already installed it, refer to the [Docker Compose Installation Guide](https://docs.docker.com/compose/install/) for instructions.

### 3. Start the Docker Container
Start the Docker container by running the following command. This command will launch three services defined in the docker-compose file:
- A PostgreSQL database,
- A Prefect server accessible at: `http://0.0.0.0:4200/`,
- A CLI environment with all the required components installed.
```bash
docker compose up -d
```

### 4. Access the cli service
To access the CLI service, use the following command:
```bash
docker compose run cli
```

### 5. Run the Prefect flow
Inside the CLI environment, 

run the following comand to seed the csv files:
```bash
dbt seed
```

run the Prefect-dbt-flow using the following command:
```bash
python my_prefect_dbt_flow.py
```
This command will execute the Prefect flow and print its status to the terminal.

### 6. View the reseults
To view the results and monitor the flow, follow these steps:

- Open a web browser and go to `http://0.0.0.0:4200/`.
- In the Prefect Server interface, click on the flow run. It should have a similar name to `adjective-animal`.
- From there, you can explore the dbt job DAG and its associated logs.

With these steps, you can set up and run a Prefect-dbt-flow and monitor its progress through the Prefect Server interface.

# How does it works?

## Installation
Before using Prefect-dbt-flow, you need to install the library. You can do this using pip:
```shell
pip install prefect-dbt-flow
```
You can install an specific version of **Prefect** if you need to:
```shell
pip install prefect==2.13.5
```

## Creating a Prefect Flow
To get started, you'll need to create a Prefect flow that incorporates your dbt project. Here's a step-by-step guide:
1. **Import the Required Modules:**
    Start by importing the necessary modules from prefect_dbt_flow:
    ```python
    from prefect_dbt_flow import dbt_flow
    ```
2. **Define the Prefect Flow:**
    Create a Prefect flow by initializing a `dbtFlow.dbt_flow` object. You can configure it with your dbt project, profile, and additional options:
    * **project**: A DbtProject object representing the dbt project configuration.
    * **profile**: A DbtProfile object representing the dbt profile configuration.
    * **dag_options**: A DbtDagOptions object to specify dbt DAG configurations.
    * **flow_kwargs**: A dictionary of Prefect flow arguments.
    Here's a basic example of how to use dbt_flow():
    ```python
    my_flow = dbtFlow.dbt_flow(
        project=dbtFlow.DbtProject(
            name="my_flow",
            project_dir="path_to/dbt_project",
            profiles_dir="path_to/dbt_profiles",
        ),
        profile=dbtFlow.DbtProfile(
            target="dev",
        ),
        dag_options=dbtFlow.DbtDagOptions(
            run_test_after_model=True,
        ),
    )
    ```
    With this basic setup, you have created a Prefect flow that manages your dbt project. When you run the script, Prefect will execute the dbt tasks defined in your project.
3. **Run the Flow:**
    To execute the Prefect flow, add the following code block:
    ```python
    if __name__ == "__main__":
        my_flow()
    ```
4. **Start the prefect server**
    You will need to start prefect before the run
    ```shell
    prefect server start
    ```
    You can check up the dashoard at `http://0.0.0.0:4200`
5. **Running the Prefect Flow:**
    To run the Prefect flow, simply execute your Python script:
    ```shell
    python my_prefect_dbt_flow.py
    ```
    Make sure you are in the correct directory or provide the full path to your script. Prefect will execute the dbt tasks defined in your flow, providing orchestration and monitoring capabilities.
6. **See the run**
    You will be able to see the results of the run on the prefect dashboard at `http://0.0.0.0:4200`

## Advanced Configuration
In the previous section, you configured your dbt project within the Prefect flow. Here's how you can customize the configuration further:

### Dbt Project Configuration:
You specified the name, project directory, and profiles directory when creating the DbtProject object. Adjust these values to match your dbt project's setup.
- `DbtProject`: Represents your dbt project configuration.
    - `name`: Name of the dbt project.
    - `project_dir`: Path to the directory containing the project.yml configuration file.
    - `profiles_dir`: Path to the directory containing the profiles.yml file.

### Dbt Profile Configuration:
The DbtProfile object allows you to set the target profile for your dbt project. This profile should match the configuration in your dbt profiles.yml file.
- `DbtProfile`: Represents the dbt profile configuration.
    - `target`: Specify the dbt target (e.g., "dev" or "prod").

### Dag Options:
The DbtDagOptions object lets you define various options for your dbt workflow. In the provided example, we set run_test_after_model to True, indicating that dbt tests should run after each dbt model.
- `DbtDagOptions`: Allows you to specify dbt DAG configurations.
    - `select`: Specify a dbt module to include in the run.
    - `exclude`: Specify a dbt module to exclude in the run.
    - `run_test_after_model`: Set this to True to run tests after running models.

### Prefect flow configuration
Prefect-dbt-flow integrates with Prefect's monitoring and error handling capabilities. You can use Prefect features like scheduling, notifications, and task retries to monitor and manage your dbt flows effectively. You can pass this additional Prefect flow configuration options using a dictionary into: `flow_kwargs`.

For more information on these features, consult the [Prefect documentation.](https://docs.prefect.io/2.10.12/api-ref/prefect/flows/#prefect.flows.flow)

## Conclusion
Prefect-dbt-flow simplifies the orchestration and management of dbt workflows within a Prefect flow. By following the steps in this guide, you can easily create and execute data pipelines that incorporate dbt projects. Be aware of breaking changes as this library is actively developed, and consult the changelog for updates. Happy data engineering! :rocket: