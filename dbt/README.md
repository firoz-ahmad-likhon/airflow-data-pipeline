# dbt

This dbt project transforms the raw Airflow ingestion table into analytics-ready models for BMRS data.

For now, dbt is run manually with Docker Compose. Airflow currently handles ingestion only. A dedicated Airflow DAG for dbt orchestration may be added later once the transformation design is stable.

## Commands

```
dbt clean
dbt deps
dbt parse
dbt build
dbt run --select +wind_and_solar_power --vars "{lookback_hours: 12}"
dbt test --select wind_and_solar_power
```

## Selector reference

- `+my_model`: include upstream dependencies.
- `my_model+`: include downstream dependents.
- `+my_model+`: include both upstream and downstream nodes.
