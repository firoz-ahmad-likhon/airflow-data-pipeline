# dbt

This dbt project transforms the raw Airflow ingestion table into analytics-ready models for BMRS data.

For now, dbt is run manually with Docker Compose. Airflow currently handles ingestion only. A dedicated Airflow DAG for dbt orchestration may be added later once the transformation design is stable.

## Commands

```
dbt clean
dbt deps
dbt parse
dbt build
dbt run
dbt run --select +wind_and_solar_power --vars "{lookback_hours: 12}"
dbt run --select tag:wind_solar
dbt test
dbt test --select wind_and_solar_power
dbt source freshness
```

## Materializations

- `view`: rebuilt each run as a view.
- `table`: rebuilt each run as a table.
- `incremental`: updates or inserts into an existing table.
- `materialized_view`: maintained as a materialized view.
- `ephemeral`: inlined into downstream models.

## Test

- `generic test`: reusable test defined once and applied in YAML.
- `singular test`: standalone SQL test for one specific check.

## Selector reference

- `+my_model`: include upstream dependencies.
- `my_model+`: include downstream dependents.
- `+my_model+`: include both upstream and downstream nodes.
