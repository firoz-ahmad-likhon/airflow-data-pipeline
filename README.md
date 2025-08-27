## Airflow Data Pipeline

This repository contains an Airflow-based data pipeline that:

- Ingests data from [API](https://bmrs.elexon.co.uk/actual-or-estimated-wind-and-solar-power-generation).
- Validates data quality using [Great Expectations](https://greatexpectations.io/).
- Stores the validated data in a Postgres database.

The pipeline is modular, reliable, and designed for extensibility in real-world data engineering workflows.

## Prerequisites
- Docker installed.

## DEV SETUP
1. Clone the repo.
2. Copy the `.env.example` to `.env` and update the values as per your environment.
3. Set `ENV=dev` in `.env`
4. Up the airflow docker containers:
   ```
   docker compose up -d --build
   ```

## PROD SETUP
1. Clone the repo.
2. Copy the `.env.example` to `.env` and update the values as per your environment.
3. Set `ENV=prod` in `.env`
4. Up the airflow docker containers:
   ```
   docker compose -f compose.yml up -d --build
   ```

## Precautions
Remove `config` and `dags/quality/gx` folders if any error occurs during the setup. To clean up the log remove `logs` folder.

## Dag run
- When you trigger the dag manually, the input date time will UTC time.
- When you trigger the backfill dag, the input date time will be in the local time zone. So, output will be converted to UTC time.
- Logical time is in UTC time.

## Testing
It is recommended to perform unit test before commiting the code. To run unit test, ensure `ENV=dev` in `.env`.

To access the server:
```
docker compose exec -it airflow-apiserver bash
```
and run the following command:

```
pytest
```

The test contains the following:
1. Integrity test on the Dag.
2. Unit test on the Dag tasks.
3. Unit test on every relevant function.

Basic test:
```
python dags/dag_psr_sync.py
```

Task test:
```
airflow tasks test  psr_sync parameterize
```
**Note:** The `parameterize` is the task name in the dag. Switch to other task name it needed.

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
```
Enable:
```
pre-commit install
```

## Great Expectations
Great Expectations will run automatically.

To init the expectations:
```
python dags/quality/gx_cli.py --mode init
```
To re-create the expectations:
```
python dags/quality/gx_cli.py --mode recreate
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
