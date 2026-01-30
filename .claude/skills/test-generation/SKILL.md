---
name: test-generation
description: Generates unit tests for Python code using pytest. Use when the user wants tests, asks for test coverage, or mentions testing a function or module.
---

# Test Generation

## Structure

```python
import pytest
from module import function_to_test

class TestFunctionName:
    """Tests for function_name."""
    
    def test_basic_case(self):
        """Test normal expected behavior."""
        result = function_to_test(valid_input)
        assert result == expected_output
    
    def test_edge_case(self):
        """Test boundary conditions."""
        ...
    
    def test_error_handling(self):
        """Test invalid inputs raise appropriate errors."""
        with pytest.raises(ValueError):
            function_to_test(invalid_input)
```

## Coverage Checklist

- [ ] Happy path (normal inputs)
- [ ] Edge cases (empty, zero, None, boundary values)
- [ ] Error cases (invalid types, out of range)
- [ ] Return value verification
- [ ] Side effects (if any)

## Naming Convention

`test_<what>_<condition>_<expected>`

Examples:
- `test_calculate_total_with_discount_returns_reduced_price`
- `test_parse_date_invalid_format_raises_valueerror`
- `test_get_user_not_found_returns_none`

## Fixtures

Use fixtures for repeated setup:

```python
@pytest.fixture
def sample_user():
    return User(name="Test", email="test@example.com")

def test_user_display_name(sample_user):
    assert sample_user.display_name == "Test"
```

## Guidelines

- One assertion per test (when practical)
- Descriptive test names over comments
- Test behavior, not implementation
- Mock external dependencies
- Keep tests fast and independent
