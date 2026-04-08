from typing import Any

import pytest

from airflow.models import DagBag


@pytest.fixture(scope="module")
def dag_wind_and_solar_power_generation() -> DagBag | Any:
    """Initialize the wind_and_solar_power_generation DAG."""
    bag = DagBag().get_dag("wind_and_solar_power_generation")
    bag.id = "wind_and_solar_power_generation"

    return bag
