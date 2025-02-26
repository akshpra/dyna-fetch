"""Test Q class (filter)."""

from datetime import date

import pytest

from dyna_fetch import Q


class TestFilters:
    """Test filters module from dyna fetch library."""

    def test_int_filters(self) -> None:
        """Test int filter."""
        # Test int
        assert Q.eq("field", 1) == "field eq 1"
        assert Q.ne("field", 1) == "field ne 1"
        assert Q.gt("field", 1) == "field gt 1"
        assert Q.lt("field", 1) == "field lt 1"
        assert Q.ge("field", 1) == "field ge 1"
        assert Q.le("field", 1) == "field le 1"
        assert Q.contains("field", 1) == "contains(field, 1)"
        assert Q.startswith("field", 1) == "startswith(field, 1)"
        assert Q.endswith("field", 1) == "endswith(field, 1)"

    def test_float_filters(self) -> None:
        """Test float filter."""
        assert Q.eq("field", 1.9) == "field eq 1.9"
        assert Q.ne("field", 1.9) == "field ne 1.9"
        assert Q.gt("field", 1.9) == "field gt 1.9"
        assert Q.lt("field", 1.9) == "field lt 1.9"
        assert Q.ge("field", 1.9) == "field ge 1.9"
        assert Q.le("field", 1.9) == "field le 1.9"
        assert Q.contains("field", 1.9) == "contains(field, 1.9)"
        assert Q.startswith("field", 1.9) == "startswith(field, 1.9)"
        assert Q.endswith("field", 1.9) == "endswith(field, 1.9)"

    def test_str_filters(self) -> None:
        """Test str filter."""
        assert Q.eq("field", "value") == "field eq 'value'"
        assert Q.ne("field", "value") == "field ne 'value'"
        assert Q.gt("field", "value") == "field gt 'value'"
        assert Q.lt("field", "value") == "field lt 'value'"
        assert Q.ge("field", "value") == "field ge 'value'"
        assert Q.le("field", "value") == "field le 'value'"
        assert Q.contains("field", "value") == "contains(field, 'value')"
        assert Q.startswith("field", "value") == "startswith(field, 'value')"
        assert Q.endswith("field", "value") == "endswith(field, 'value')"

    def test_date_filters(self) -> None:
        """Test date filter."""
        assert Q.eq("field", date(2024, 1, 1)) == "field eq 2024-01-01"
        assert Q.ne("field", date(2024, 1, 1)) == "field ne 2024-01-01"
        assert Q.gt("field", date(2024, 1, 1)) == "field gt 2024-01-01"
        assert Q.lt("field", date(2024, 1, 1)) == "field lt 2024-01-01"
        assert Q.ge("field", date(2024, 1, 1)) == "field ge 2024-01-01"
        assert Q.le("field", date(2024, 1, 1)) == "field le 2024-01-01"
        assert Q.contains("field", date(2024, 1, 1)) == "contains(field, 2024-01-01)"
        assert Q.startswith("field", date(2024, 1, 1)) == "startswith(field, 2024-01-01)"
        assert Q.endswith("field", date(2024, 1, 1)) == "endswith(field, 2024-01-01)"

    def test_bool_filters(self) -> None:
        """Test bool filter."""
        assert Q.eq("field", True) == "field eq true"
        assert Q.ne("field", True) == "field ne true"
        assert Q.gt("field", True) == "field gt true"
        assert Q.lt("field", True) == "field lt true"
        assert Q.ge("field", True) == "field ge true"
        assert Q.le("field", True) == "field le true"
        assert Q.contains("field", True) == "contains(field, true)"
        assert Q.startswith("field", True) == "startswith(field, true)"
        assert Q.endswith("field", True) == "endswith(field, true)"

    def test_invalid_filters(self) -> None:
        """Test invalid filter."""
        with pytest.raises(TypeError):
            Q.eq("admin", None)

        with pytest.raises(TypeError):
            Q.ne("admin", None)

        with pytest.raises(TypeError):
            Q.gt("admin", None)

        with pytest.raises(TypeError):
            Q.ge("admin", None)

        with pytest.raises(TypeError):
            Q.lt("admin", None)

        with pytest.raises(TypeError):
            Q.le("admin", None)

        with pytest.raises(TypeError):
            Q.contains("admin", None)

        with pytest.raises(TypeError):
            Q.startswith("admin", None)

        with pytest.raises(TypeError):
            Q.endswith("admin", None)

    def test_and_group_filters(self) -> None:
        """Test AND group filter."""
        filter1 = Q.eq("field1", 100)
        filter2 = Q.ne("field1", 100)
        assert Q.and_group(filter1, filter2) == "(field1 eq 100 and field1 ne 100)"
        with pytest.raises(ValueError):
            assert Q.and_group()

    def test_or_group_filters(self) -> None:
        """Test OR group filter."""
        filter1 = Q.eq("field1", 100)
        filter2 = Q.ne("field1", 100)
        assert Q.or_group(filter1, filter2) == "(field1 eq 100 or field1 ne 100)"
        with pytest.raises(ValueError):
            assert Q.or_group()
