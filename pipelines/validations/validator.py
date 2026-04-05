from abc import ABC, abstractmethod


class Validator(ABC):
    """Abstract class for validators."""

    @abstractmethod
    def validate(self) -> bool:
        """To identify if the validations passed."""
        pass
