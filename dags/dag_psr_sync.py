import logging
import pendulum
from typing import Any, cast
from airflow.exceptions import AirflowException
from airflow.sdk import dag, task, task_group
from airflow.sdk import Param
from airflow.sdk import Label
from airflow.utils.trigger_rule import TriggerRule
from airflow.utils.types import DagRunType
from airflow.models import DagRun
from dags.database.connection import DBConnection
from dags.database.models import PSR
from dags.services.source import SourceAPI as Source
from dags.utils.api_helper import APIHelper as Helper
from dags.validations.parameter_validation import ParameterValidator as Validator
from sqlalchemy.dialects.postgresql import insert

# Use the Airflow task logger
logger = logging.getLogger("dag_psr_sync")

# Default date for parameter
DEFAULT_DATE = Helper.floored_to_30_min(pendulum.now(tz="UTC")).to_iso8601_string()


@dag(
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
    description="An ETL DAG for sync Actual or estimated wind and solar power generation data from API to PostgreSQL",
)
def psr_sync() -> None:
    """ETL DAG for psr data."""

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

    @task_group(group_id="Processor", tooltip="Data processing unit")
    def source(parameters: dict[str, str]) -> Any:
        """Tasks group for processing source data."""

        @task(task_display_name="Fetcher")
        def fetch(p: dict[str, str]) -> dict[str, Any]:
            """Fetch the JSON data from the API and push it to XCom for downstream tasks."""
            try:
                data = Source().fetch_json(
                    cast(pendulum.DateTime, p["date_from"]),
                    cast(pendulum.DateTime, p["date_to"]),
                )

                if not data["data"]:
                    raise AirflowException("Data is empty")
                logger.info("Data fetch successful")
                return data
            except Exception as e:
                raise AirflowException(f"Data fetch failed: {e}") from e

        @task(task_display_name="Transformer")
        def transform(data: dict[str, Any]) -> list[tuple[str, str, float]]:
            """Transform the JSON data into a format suitable for bulk insert into the destination table."""
            return Helper.transform(data)

        fetched_data = fetch(parameters)
        transformed_data = transform(cast(dict[str, Any], fetched_data))

        (
            fetched_data
            >> Label("Fetched data from API")
            >> transformed_data
            >> Label("Transformed data")
        )

        return transformed_data

    @task(task_display_name="Sync data to destination table")
    def sync(data: list[tuple[str, str, float]]) -> bool:
        """Perform the bulk insert of the JSON data into the destination table."""
        try:
            con = DBConnection()
            with con.get_session() as db:
                records = [
                    {
                        "curve_name": row[0],
                        "curve_date": row[1],
                        "value": row[2],
                    }
                    for row in data
                ]
                # Build UPSERT statement for postgres
                stmt = insert(PSR).values(records)
                stmt = stmt.on_conflict_do_update(
                    index_elements=["curve_name", "curve_date"],
                    set_={"value": stmt.excluded.value},  # update the value if conflict
                )

                db.execute(stmt)
                db.commit()
            logger.info("Data sync successful")
            return True
        except Exception as e:
            raise AirflowException(f"Data sync failed: {e}") from e

    @task(trigger_rule=TriggerRule.ONE_FAILED, retries=0)
    def watcher() -> None:
        """Raise an exception if one or more upstream tasks failed."""
        raise AirflowException(
            "Failing task because one or more upstream tasks failed.",
        )

    # Set up dependencies for TaskGroups and tasks
    parameterized = parameterize()  # type: ignore
    fetched = source(cast(dict[str, str], parameterized))
    synced = sync(cast(list[tuple[str, str, float]], fetched))

    fetched >> Label("Transformed data") >> synced

    [parameterized, fetched, synced] >> Label("Fail") >> watcher()


# Instantiate the DAG
psr_sync()
