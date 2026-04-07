## Airflow Data Pipeline

This repository contains an Airflow-based data pipeline that:

- Ingests data from [API](https://bmrs.elexon.co.uk/actual-or-estimated-wind-and-solar-power-generation).
- Stores data in a Postgres database.

The pipeline is modular, reliable, and designed for extensibility in real-world data engineering workflows.

## Prerequisites
- Docker installed.

## Development
1. Clone the repo.
2. Copy the `.env-example` to `.env` and update the values as per your environment.
3. Set `ENV=dev` in `.env`
4. Up the airflow docker containers:
   ```
   docker compose --env-file .env -f infra/compose.yml -f infra/compose.override.yml up -d --build
   ```

## Dag run
- When you trigger the dag manually, the input date time will UTC time.
- When you trigger the backfill dag, the input date time will be in the local time zone. So, output will be converted to UTC time.
- Logical time is in UTC time.

## Testing
It is recommended to perform unit test before commiting the code. To run unit test, ensure `ENV=dev` in `.env`.

Pytest:

```
docker compose --env-file .env -f infra/compose.yml -f infra/compose.override.yml exec airflow-apiserver pytest
```

DAG loader test:

```
python dags/wind_and_solar_power_generation.py
```

```
time python dags/wind_and_solar_power_generation.py
```

Dag Run test:
```
airflow dags test wind_and_solar_power_generation
```
params: `--conf '{"date_from":"2025-01-01T00:00:00Z","date_to":"2025-01-01T00:30:00Z"}'`

Task test:
```
airflow tasks test wind_and_solar_power_generation parameterize
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

## Production
1. Clone the repo.
2. Copy the `.env-example` to `.env` and update the values as per your environment.
3. Set `ENV=prod` in `.env`
4. Set `IMAGE_TAG` in `.env` (for example, `IMAGE_TAG=v1.0.0`).
5. Pull the image:
   ```
   docker compose --env-file .env -f infra/compose.yml pull
   ```
6. Up the airflow docker containers:
   ```
   docker compose --env-file .env -f infra/compose.yml up -d
   ```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
