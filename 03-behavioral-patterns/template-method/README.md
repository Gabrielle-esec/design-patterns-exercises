# Template Method Pattern — Data ETL Pipeline

## Problem

The original CSV, API and Database pipelines repeated
the same workflow: connect, extract, transform, validate,
load and cleanup.

This duplication made maintenance difficult. Any change
to the workflow had to be repeated across several classes.

## Solution

The Template Method pattern centralizes the workflow
in the abstract DataPipeline class.

The run() method executes the steps in a fixed order:
1. Connect
2. Extract
3. Transform
4. Validate
5. Before-load hook
6. Load
7. Cleanup

The concrete pipelines implement source-specific behavior:

- CSVPipeline: transforms user records from CSV data.
- APIPipeline: processes API user data and assigns grades.
- DatabasePipeline: processes product data and calculates tax.
- XMLPipeline: demonstrates how to add a new data source.

Validation and cleanup are shared in the base class.
The optional before_load() hook allows customization.

Cleanup runs in a finally block, even when an error occurs.

## Design benefits

- Common workflow defined once
- Reduced code duplication
- Consistent execution order
- Reusable validation and cleanup
- Easy to introduce new pipeline types
- Easier maintenance and testing

## UML diagram

See [uml.md](uml.md).

## Run the demonstration

From the repository root:

    python3 -B 03-behavioral-patterns/template-method/data_pipeline.py

## Run the tests

From the template-method directory:

    python3 -B -m unittest -v

## Note

The input data and connections are simulated, as in
the original exercise. No real database or API is accessed.
