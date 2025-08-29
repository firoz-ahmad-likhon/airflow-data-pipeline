import pytest
from typing import Any


@pytest.fixture(scope="session")
def mock_data() -> dict[str, list[dict[str, Any]]]:
    """Fixture to provide mock data for testing."""
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
