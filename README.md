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
3. Up the airflow docker containers:
   ```
   docker-compose up -d --build
   ```
4.  [airflow UI](http://localhost:8080). The credentials are `airflow` and `airflow`.
5. To access the server:
   ```
   docker-compose exec -it airflow-webserver bash
   ```

## Testing
It is recommended to perform unit test before commiting the code. To run unit test, run the following command:

`pytest`

The test contains the following:
1. Integrity test on the Dag.
2. Unit test on the Dag tasks.
3. Unit test on every relevant function.

Basic test:
```
python dags/dag_psr_sync.py
```

Debugging:
Change the dag call `psr_sync()` to
```
if __name__ == "__main__":
    psr_sync().test()
```
and then run:
```
python dags/dag_psr_sync.py
```


## Type Checking and Linting
This repo uses `pre-commit` hooks to check type and linting before committing the code.

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
