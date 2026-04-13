# Airflow DBT Pipeline

## Problem
The data from BMRS ELEXON API has three practical issues for analytics:

- Data is delayed by about 90 minutes.
- The response is nested JSON, which is difficult to use directly in BI tools and SQL analysis.
- The source may republish corrected data, so analytics can become inconsistent unless data is reprocessed or backfilled.

This becomes a real business problem when teams want trusted metrics such as peak generation, daily average generation,
and 7-day rolling average generation. If each team calculates those differently, reporting starts to drift.

## Solution

This project uses a simple modern analytics pattern:

- Airflow orchestrates the pipeline end to end: it pulls raw data from the [API](https://bmrs.elexon.co.uk/api-documentation/) on a schedule and can also orchestrate the dbt transformation pipeline.
- Raw snapshots are kept first, which makes late-arriving or revised records safe to reprocess.
- dbt transforms the nested JSON into a clean model with the latest generation quantity by `start_time` and `psr_type`.
- A configurable lookback window allows recent data to be rebuilt like a controlled backfill when the source is delayed.

Ingesting api endpoints:
1. [Wind and Solar Power](https://bmrs.elexon.co.uk/actual-or-estimated-wind-and-solar-power-generation)

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
