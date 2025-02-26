"""OData filters."""

from datetime import date
from typing import Any


def _sanitize_value(value: Any) -> str:
    """Sanitize the value based on value type."""
    # Bool first because bool resolves to int
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, int | float):
        return str(value)
    if isinstance(value, str):
        return f"'{value}'"
    raise TypeError(f"Filtering on type {type(value).__name__} is not supported.")


class Q:
    """Class to hold all filter types."""

    @staticmethod
    def eq(field: str, value: Any) -> str:
        """Equal filter function."""
        value = _sanitize_value(value)
        return f"{field} eq {value}"

    @staticmethod
    def ne(field: str, value: Any) -> str:
        """Not equal filter function."""
        value = _sanitize_value(value)
        return f"{field} ne {value}"

    @staticmethod
    def lt(field: str, value: Any) -> str:
        """Less than filter function."""
        value = _sanitize_value(value)
        return f"{field} lt {value}"

    @staticmethod
    def gt(field: str, value: Any) -> str:
        """Greater than filter function."""
        value = _sanitize_value(value)
        return f"{field} gt {value}"

    @staticmethod
    def le(field: str, value: Any) -> str:
        """Less than or equal filter function."""
        value = _sanitize_value(value)
        return f"{field} le {value}"

    @staticmethod
    def ge(field: str, value: Any) -> str:
        """Greater than or equal filter function."""
        value = _sanitize_value(value)
        return f"{field} ge {value}"

    @staticmethod
    def contains(field: str, value: Any) -> str:
        """Contains filter function."""
        value = _sanitize_value(value)
        return f"contains({field}, {value})"

    @staticmethod
    def startswith(field: str, value: Any) -> str:
        """Startswith filter function."""
        value = _sanitize_value(value)
        return f"startswith({field}, {value})"

    @staticmethod
    def endswith(field: str, value: Any) -> str:
        """Startswith filter function."""
        value = _sanitize_value(value)
        return f"endswith({field}, {value})"

    @staticmethod
    def and_group(*conditions: str) -> str:
        """Filter group joined by and operator."""
        valid_conditions = [c for c in conditions if c]
        if not valid_conditions:
            raise ValueError("At least one condition must be given for AND group.")
        return f"({' and '.join(valid_conditions)})"

    @staticmethod
    def or_group(*conditions: str) -> str:
        """Filter group joined by or operator."""
        valid_conditions = [c for c in conditions if c]
        if not valid_conditions:
            raise ValueError("At least one condition must be given for OR group.")
        return f"({' or '.join(valid_conditions)})"
