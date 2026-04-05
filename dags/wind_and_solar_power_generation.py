import logging
from typing import Any

import pendulum
from airflow.exceptions import AirflowException
from airflow.models import DagRun
from airflow.sdk import Param, dag, task
from airflow.utils.types import DagRunType
from sqlalchemy import insert

from dags.database.connection import DBConnection
from dags.database.models import WindAndSolarPowerGeneration
from dags.services.source import SourceAPI as Source
from dags.utils.api_helper import APIHelper as Helper
from dags.validations.parameter_validation import ParameterValidator as Validator

# Use the Airflow task logger
logger = logging.getLogger("dag_wind_and_solar_power_generation")

# Default date for parameter
DEFAULT_DATE = Helper.floored_to_30_min(pendulum.now(tz="UTC")).to_iso8601_string()


@dag(
    dag_id="wind_and_solar_power_generation",
    schedule="5,35 * * * *",  # Run at minute 5 and 35 of every hour
    start_date=pendulum.datetime(2025, 5, 10, 10, 45, 0, tz="UTC"),
    catchup=False,
    tags=["half hourly"],
    default_args={
        "retries": 1,
        "retry_delay": pendulum.duration(minutes=5),
    },
    params={
        "date_from": Param(
            default=DEFAULT_DATE,
            type="string",
            format="date-time",
            description="Date From",
        ),
        "date_to": Param(
            default=DEFAULT_DATE,
            type="string",
            format="date-time",
            description="Date To",
        ),
    },
    description="An ETL DAG for syncing raw wind and solar power generation API payloads to PostgreSQL",
)
def wind_and_solar_power_generation() -> None:
    """ETL DAG for wind and solar power generation data."""

    @task(task_display_name="Parameterize the dates", retries=0)
    def parameterize(params: dict[str, Any], dag_run: DagRun) -> dict[str, Any]:
        """Validate the dates and return valid dates or raise an exception."""
        run_type = dag_run.run_type
        logical_date = pendulum.instance(
            dag_run.logical_date or pendulum.now(tz="UTC"),
        )  # testing may not have a logical date

        if run_type == DagRunType.MANUAL:
            # Validate user-provided params
            validator = Validator(params["date_from"], params["date_to"])
            if not validator.validate():
                raise AirflowException(validator.errors[-1])
            date_from = Helper.floored_to_30_min(validator.date_from)
            date_to = Helper.floored_to_30_min(validator.date_to)

        elif run_type == DagRunType.BACKFILL_JOB:
            date_from = date_to = Helper.floored_to_30_min(logical_date)

        else:
            # Default case: scheduled, etc.
            date_from = date_to = Helper.date_param(logical_date)

        return {
            "date_from": date_from,
            "date_to": date_to,
        }

    @task(task_display_name="Extract")
    def extract(p: dict[str, Any]) -> dict[str, Any]:
        """Fetch the JSON data from the API and push it to XCom for downstream tasks."""
        try:
            data = Source().fetch_json(
                p["date_from"],
                p["date_to"],
            )
            logger.info("Data fetch successful")
            return data
        except Exception as e:
            raise AirflowException(f"Data fetch failed: {e}") from e

    @task(task_display_name="Load")
    def load(data: dict[str, Any]) -> bool:
        """Load the raw record into the destination table."""
        try:
            con = DBConnection()
            with con.get_session() as db:
                record = {
                    "ingestion_ts": pendulum.parse(data["ingestion_ts"]),
                    "window_from_utc": pendulum.parse(data["window_from_utc"]),
                    "window_to_utc": pendulum.parse(data["window_to_utc"]),
                    "request_url": data["request_url"],
                    "http_status": data["http_status"],
                    "payload_json": data["payload_json"],
                    "load_date": pendulum.parse(data["load_date"]).date(),
                }
                stmt = insert(WindAndSolarPowerGeneration).values(record)
                db.execute(stmt)
                db.commit()
            logger.info("Data sync successful")
            return True
        except Exception as e:
            raise AirflowException(f"Data sync failed: {e}") from e

    parameterized = parameterize()  # type: ignore
    extracted = extract(parameterized)
    load(extracted)


# Instantiate the DAG
wind_and_solar_power_generation()
