from airflow.models import DagBag

from tests.interface.integrity_tester import IntegrityTester


class TestWindAndSolarPowerGenerationDAG(IntegrityTester):
    """Test the wind_and_solar_power_generation DAG."""

    def test_dag_loaded(self, dag_wind_and_solar_power_generation: DagBag) -> None:
        """Test if the DAG is correctly loaded."""
        assert DagBag().import_errors == {}, "Improper import"
        assert dag_wind_and_solar_power_generation.id in DagBag().dags, f"DAG '{dag_wind_and_solar_power_generation.id}' is missing"
        assert dag_wind_and_solar_power_generation is not None, "DAG object is None"
        assert len(dag_wind_and_solar_power_generation.tasks) > 0, "No tasks in the DAG"

    def test_dag_has_tag(self, dag_wind_and_solar_power_generation: DagBag) -> None:
        """Test if the DAG contains the correct tag."""
        assert "half hourly" in dag_wind_and_solar_power_generation.tags, "Tag 'half hourly' is missing in the DAG"

    def test_task_count(self, dag_wind_and_solar_power_generation: DagBag) -> None:
        """Test the number of tasks in the DAG."""
        expected_task_count = 3
        assert len(dag_wind_and_solar_power_generation.tasks) == expected_task_count, f"Expected 3 tasks, but got {len(dag_wind_and_solar_power_generation.tasks)}"

    def test_task_dependencies(self, dag_wind_and_solar_power_generation: DagBag) -> None:
        """Test the dependencies between the tasks."""
        # Define expected upstream and downstream dependencies
        task_deps = {
            "extract": ["parameterize"],
            "load": ["extract"],
        }

        for task_id, upstream_ids in task_deps.items():
            task = dag_wind_and_solar_power_generation.get_task(task_id)
            assert task is not None, f"Task '{task_id}' is missing in the DAG"
            upstream_tasks = [t.task_id for t in task.upstream_list]
            assert set(upstream_ids) == set(
                upstream_tasks,
            ), f"Task '{task_id}' has incorrect upstream dependencies"
