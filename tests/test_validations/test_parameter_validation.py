from dags.validations.parameter_validation import ParameterValidator
import pytest


class TestParameterValidator:
    """Test the parameter validator class."""

    def test_valid_dates(self, parameter_validator: ParameterValidator) -> None:
        """Test valid dates.

        :param parameter_validator: ParameterValidator instance from fixture.
        """
        assert len(parameter_validator.errors) == 0

    def test_date_order(self, parameter_validator: ParameterValidator) -> None:
        """Test date order.

        :param parameter_validator: ParameterValidator instance from fixture.
        """
        assert parameter_validator.validate_date_order() is True

    def test_days_range(self, parameter_validator: ParameterValidator) -> None:
        """Test days range.

        :param parameter_validator: ParameterValidator instance from fixture.
        """
        assert parameter_validator.validate_days_range() is True

    def test_valid_minutes(self, parameter_validator: ParameterValidator) -> None:
        """Test valid minutes.

        :param parameter_validator: ParameterValidator instance from fixture.
        """
        assert parameter_validator.validate_minutes() is True

    def test_invalid_date(
        self,
        parameter_validator_with_invalid_dates: ParameterValidator,
    ) -> None:
        """Test invalid date.

        :param parameter_validator_with_invalid_dates: ParameterValidator instance with invalid dates from fixture.
        """
        assert len(parameter_validator_with_invalid_dates.errors) == 1

    def test_date_order_exceeds_limit(
        self,
        parameter_validator: ParameterValidator,
    ) -> None:
        """Test date order exceeds limit.

        :param parameter_validator: ParameterValidator instance from fixture.
        """
        parameter_validator.date_from = parameter_validator.date_from.add(days=10)
        assert parameter_validator.validate_date_order() is False

    def test_days_range_exceeds_limit(
        self,
        parameter_validator: ParameterValidator,
    ) -> None:
        """Test days range exceeds limit.

        :param parameter_validator: ParameterValidator instance from fixture.
        """
        assert parameter_validator.validate_days_range() is True

    def test_invalid_minutes(self, parameter_validator: ParameterValidator) -> None:
        """Test invalid minutes.

        :param parameter_validator: ParameterValidator instance from fixture.
        """
        parameter_validator.date_from = parameter_validator.date_from.add(minutes=8)
        assert parameter_validator.validate_minutes() is False

    @pytest.mark.parametrize(
        ("dirty", "expected"),
        [
            ("2025-05-20T12:00:00.123Z:00+00", "2025-05-20T12:00:00Z"),
            ("2025-05-20T12:00:00.000Z", "2025-05-20T12:00:00Z"),
            ("2025-05-20T12:00:00+00:00", "2025-05-20T12:00:00Z"),
            ("2025-05-20T12:00:00.456+00:00", "2025-05-20T12:00:00Z"),
        ],
    )
    def test_clean_date_param(self, dirty: str, expected: str) -> None:
        """Test clean date parameter.

        :param dirty: Dirty date.
        :param expected: Expected clean date.
        """
        assert ParameterValidator.clean(dirty) == expected
