# dbt

This dbt project transforms the raw Airflow ingestion table into analytics-ready models for wind and solar power generation.


## Commands

```
dbt clean
dbt deps
dbt parse
dbt build
dbt run --select wind_and_solar_generation --vars "{lookback_hours: 12}"
dbt test --select wind_and_solar_generation
```
