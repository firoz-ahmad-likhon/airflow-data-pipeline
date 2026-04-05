from datetime import datetime, timezone

import pendulum

from pipelines.utils.api_helper import APIHelper


class TestAPIHelper:
    """Test class for APIHelper."""

    def test_date_param(self) -> None:
        """Test the date_param method."""
        assert APIHelper.date_param(
            pendulum.instance(datetime(2024, 10, 16, 10, 45, tzinfo=timezone.utc)),
        ) == pendulum.instance(datetime(2024, 10, 16, 9, 0, tzinfo=timezone.utc))

    def test_floored_to_30_min(self) -> None:
        """Test the floored_to_30_min method."""
        assert APIHelper.floored_to_30_min(
            pendulum.instance(datetime(2024, 10, 16, 10, 45, tzinfo=timezone.utc)),
        ) == pendulum.instance(datetime(2024, 10, 16, 10, 30, tzinfo=timezone.utc))
