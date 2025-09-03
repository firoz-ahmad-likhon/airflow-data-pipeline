from typing import Any
import pytest
from dags.validations.parameter_validation import ParameterValidator


@pytest.fixture
def parameter_validator(mock_params: dict[str, Any]) -> ParameterValidator:
    """Initialize the ParameterValidator."""
    return ParameterValidator(mock_params["date_from"], mock_params["date_to"])


@pytest.fixture
def parameter_validator_with_invalid_dates() -> ParameterValidator:
    """Initialize the ParameterValidator."""
    return ParameterValidator("invalid", "2024-10-16 00:30")
