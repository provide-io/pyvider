import pytest

from pyvider.components.data_sources.env_variables import (
    EnvVariablesConfig,
    EnvVariablesDataSource,
)
from pyvider.exceptions import DataSourceError
from pyvider.resources.context import ResourceContext


@pytest.fixture
def mock_environ(monkeypatch):
    """A pytest fixture to set up a controlled os.environ for tests."""
    env = {
        "TEST_VAR1": "Value1",
        "TEST_VAR2": "Value2",
        "TEST_SENSITIVE": "secret-token",
        "test_lower_case": "lower",
        "TEST_EMPTY": "",
        "ANOTHER_VAR": "another",
        "REGEX_TEST_VARX": "This matches",
    }
    monkeypatch.setattr("os.environ", env)
    return env

@pytest.fixture
def data_source() -> EnvVariablesDataSource:
    """Provides a fresh instance of the data source for each test."""
    return EnvVariablesDataSource()

@pytest.mark.asyncio
class TestEnvVariablesDataSource:
    """Comprehensive test suite for the EnvVariablesDataSource."""

    async def test_read_no_config_raises_error(self, data_source: EnvVariablesDataSource):
        """Verify that calling read with a null config raises a DataSourceError."""
        ctx = ResourceContext(config=None)
        with pytest.raises(DataSourceError, match="Configuration is required"):
            await data_source.read(ctx)

    async def test_filter_by_keys(self, data_source: EnvVariablesDataSource, mock_environ):
        config = EnvVariablesConfig(keys=["TEST_VAR1", "test_lower_case", "NOT_A_VAR"])
        ctx = ResourceContext(config=config)
        state = await data_source.read(ctx)
        assert state.all_values == {"TEST_VAR1": "Value1", "test_lower_case": "lower"}
        assert state.values == state.all_values
        assert state.sensitive_values == {}

    async def test_filter_by_prefix_case_sensitive(self, data_source: EnvVariablesDataSource, mock_environ):
        config = EnvVariablesConfig(prefix="TEST_")
        ctx = ResourceContext(config=config)
        state = await data_source.read(ctx)
        assert "TEST_VAR1" in state.all_values
        assert "TEST_VAR2" in state.all_values
        assert "TEST_SENSITIVE" in state.all_values
        assert "test_lower_case" not in state.all_values
        assert "ANOTHER_VAR" not in state.all_values

    async def test_filter_by_prefix_case_insensitive(self, data_source: EnvVariablesDataSource, mock_environ):
        config = EnvVariablesConfig(prefix="test_", case_sensitive=False)
        ctx = ResourceContext(config=config)
        state = await data_source.read(ctx)
        assert "TEST_VAR1" in state.all_values
        assert "TEST_VAR2" in state.all_values
        assert "TEST_SENSITIVE" in state.all_values
        assert "test_lower_case" in state.all_values
        assert "ANOTHER_VAR" not in state.all_values

    async def test_filter_by_regex(self, data_source: EnvVariablesDataSource, mock_environ):
        config = EnvVariablesConfig(regex=r".*VAR.*")
        ctx = ResourceContext(config=config)
        state = await data_source.read(ctx)
        assert "TEST_VAR1" in state.all_values
        assert "TEST_VAR2" in state.all_values
        assert "ANOTHER_VAR" in state.all_values
        assert "REGEX_TEST_VARX" in state.all_values

    async def test_filter_by_invalid_regex_raises_error(self, data_source: EnvVariablesDataSource, mock_environ):
        config = EnvVariablesConfig(regex="[invalid-regex")
        ctx = ResourceContext(config=config)
        with pytest.raises(DataSourceError, match="Invalid regex provided"):
            await data_source.read(ctx)

    async def test_exclude_empty_is_default(self, data_source: EnvVariablesDataSource, mock_environ):
        config = EnvVariablesConfig(keys=["TEST_VAR1", "TEST_EMPTY"])
        ctx = ResourceContext(config=config)
        state = await data_source.read(ctx)
        assert "TEST_EMPTY" not in state.all_values
        assert "TEST_VAR1" in state.all_values

    async def test_include_empty_when_false(self, data_source: EnvVariablesDataSource, mock_environ):
        config = EnvVariablesConfig(keys=["TEST_VAR1", "TEST_EMPTY"], exclude_empty=False)
        ctx = ResourceContext(config=config)
        state = await data_source.read(ctx)
        assert "TEST_EMPTY" in state.all_values
        assert state.all_values["TEST_EMPTY"] == ""

    async def test_key_and_value_transformations(self, data_source: EnvVariablesDataSource, mock_environ):
        config = EnvVariablesConfig(
            keys=["TEST_VAR1", "test_lower_case"],
            transform_keys="upper",
            transform_values="lower"
        )
        ctx = ResourceContext(config=config)
        state = await data_source.read(ctx)
        expected = {"TEST_VAR1": "value1", "TEST_LOWER_CASE": "lower"}
        assert state.all_values == expected

    async def test_sensitive_keys_separation(self, data_source: EnvVariablesDataSource, mock_environ):
        config = EnvVariablesConfig(
            keys=["TEST_VAR1", "TEST_SENSITIVE"],
            sensitive_keys=["TEST_SENSITIVE"]
        )
        ctx = ResourceContext(config=config)
        state = await data_source.read(ctx)
        assert state.values == {"TEST_VAR1": "Value1"}
        assert state.sensitive_values == {"TEST_SENSITIVE": "secret-token"}
        assert state.all_values == {"TEST_VAR1": "Value1", "TEST_SENSITIVE": "secret-token"}

    async def test_all_environment_capture(self, data_source: EnvVariablesDataSource, mock_environ):
        config = EnvVariablesConfig(keys=["TEST_VAR1"])
        ctx = ResourceContext(config=config)
        state = await data_source.read(ctx)
        assert state.all_environment == mock_environ

    async def test_validation_allows_single_filter(self, data_source: EnvVariablesDataSource):
        assert await data_source.validate(EnvVariablesConfig(keys=["A"])) == []
        assert await data_source.validate(EnvVariablesConfig(prefix="A")) == []
        assert await data_source.validate(EnvVariablesConfig(regex="A")) == []

    async def test_validation_rejects_multiple_filters(self, data_source: EnvVariablesDataSource):
        errors = await data_source.validate(EnvVariablesConfig(keys=["A"], prefix="B"))
        assert len(errors) == 1
        assert "Only one of 'keys', 'prefix', or 'regex' can be specified" in errors[0]
