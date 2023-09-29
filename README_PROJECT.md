# Prefect Integration for dbt

## Overview
- **Project Duration:** 1 month
- **Sprint Duration:** 4 days
- **Goal:** Develop a fully integrated solution for running dbt models seamlessly using Prefect.
- **Primary Objective:** Make it work!
- **Tools:**
    - **dbt:** Data Transformation Tool
    - **Prefect:** Workflow Automation and Scheduling Tool
- **Deliverables:**
    - GitHub repository with code for cloning or installing as a Python package.
    - Presentation explaining how the integration works.
- **Milestones:**
    - **Development and Testing:**
    - **DEMO:** Utilize [jaffle_shop](https://github.com/dbt-labs/jaffle_shop) as an example.
    - **Presentation:**

## Team Members
- Nico Gelders
- David Valdez

## Project Description
The aim of this project is to create a Prefect integration tool for running dbt (data transformation) models, similar to how Astronomer Cosmos can be used. This integration will dynamically generate Prefect flows from dbt models, providing several benefits, including:
- Avoiding dependency conflicts
- Utilizing data-aware scheduling
- Implementing retries
- Altering workflows as needed

## Setup from python-minimal boiler plate
1. Clone this repo
2. Make sure to [install Poetry](https://python-poetry.org/docs/#installation)
3. In your project directory run
   1. `poetry shell`
   2. `poetry install`
   3. `pre-commit install`
4. On each `git commit` the code validation packages will be run before the actual commit.
5. Explore the setup in the folder structure of this package.
6. Profit.
