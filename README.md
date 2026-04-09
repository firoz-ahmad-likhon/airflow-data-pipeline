## Airflow DBT Pipeline

This repository contains Airflow-managed data pipelines that:

- Ingests data from [API](https://bmrs.elexon.co.uk/actual-or-estimated-wind-and-solar-power-generation).
- Transform data using dbt.
- Postgres storage.

The pipelines are reliable, scalable and maintainable in real-world data engineering workflows.

## Prerequisites
- Docker installed.

## Development
1. Clone the repo.
2. Copy the `.env-example` to `.env` and update the values as per your environment.
3. Set `ENV=dev` in `.env`
4. Set `IMAGE_TAG` in `.env` (for example, `IMAGE_TAG=2.0.0`)
5. Up the airflow docker containers:
   ```
   docker compose up -d --build
   ```

## Testing
It is recommended to perform unit test before commiting the code. To run unit test, ensure `ENV=dev` in `.env`.

Pytest:

```
docker compose exec airflow-apiserver pytest
```

DAG loader test:

```
docker compose exec airflow-apiserver python dags/wind_and_solar_power_generation.py
```

Dag Run test:
```
docker compose exec airflow-apiserver airflow dags test wind_and_solar_power_generation
```
params: `--conf '{"date_from":"2025-01-01T00:00:00Z","date_to":"2025-01-01T00:30:00Z"}'`

Task test:
```
docker compose exec airflow-apiserver airflow tasks test wind_and_solar_power_generation parameterize
```
params: `--task-params '{"date_from":"2025-01-01T00:00:00Z","date_to":"2025-01-01T00:30:00Z"}'`

**Note:** Available tasks: `airflow tasks list wind_and_solar_power_generation`. **Task test does not fit with existing dags**.

## Type Checking and Linting
This repo uses `pre-commit` hooks to check type and linting before committing the code.

Virtual environment:
```
python -m venv .venv
```
Activate:
```
source .venv/bin/activate
```
In Windows, use:
```
.venv\Scripts\activate
```
Install:
```
pip install pre-commit
pre-commit install
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
