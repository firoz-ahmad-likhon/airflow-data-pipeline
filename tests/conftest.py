import pytest
from typing import Any


@pytest.fixture(scope="session")
def mock_data() -> dict[str, list[dict[str, Any]]]:
    """Fixture providing mock API data."""
    return {
        "data": [
            {
                "publishTime": "2023-07-21T06:58:08Z",
                "businessType": "Wind generation",
                "psrType": "Wind Onshore",
                "quantity": 640.283,
                "startTime": "2023-07-21T04:30:00Z",
                "settlementDate": "2023-07-21",
                "settlementPeriod": 12,
            },
            {
                "publishTime": "2023-07-21T06:58:08Z",
                "businessType": "Wind generation",
                "psrType": "Wind Offshore",
                "quantity": 77.014,
                "startTime": "2023-07-21T04:30:00Z",
                "settlementDate": "2023-07-21",
                "settlementPeriod": 12,
            },
            {
                "publishTime": "2023-07-21T06:58:08Z",
                "businessType": "Solar generation",
                "psrType": "Solar",
                "quantity": 89,
                "startTime": "2023-07-21T04:30:00Z",
                "settlementDate": "2023-07-21",
                "settlementPeriod": 12,
            },
        ],
    }


@pytest.fixture(scope="session")
def mock_transformed_data() -> list[tuple[str, str, float]]:
    """Fixture providing mock transformed data."""
    return [
        ("bmreports, Wind Onshore, min30", "2023-07-21T04:30:00Z", 640.283),
        ("bmreports, Wind Offshore, min30", "2023-07-21T04:30:00Z", 77.014),
        ("bmreports, Solar, min30", "2023-07-21T04:30:00Z", 89.0),
    ]


@pytest.fixture
def mock_params() -> dict[str, Any]:
    """Fixture providing mock parameters."""
    return {
        "date_from": "2024-10-15 00:00",
        "date_to": "2024-10-16 00:30",
    }
