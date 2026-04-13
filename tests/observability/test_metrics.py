#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for pyvider metrics collection.

Tests all metrics defined in pyvider.observability.metrics module to ensure
100% test coverage of observability features."""

from pyvider.observability import (
    components_discovered,
    datasource_errors,
    datasource_read_total,
    discovery_duration,
    discovery_errors,
    ephemeral_close_total,
    ephemeral_errors,
    ephemeral_open_total,
    ephemeral_renew_total,
    function_calls,
    function_duration,
    function_errors,
    handler_duration,
    handler_errors,
    handler_requests,
    provider_configure_errors,
    provider_configure_total,
    resource_create_total,
    resource_delete_total,
    resource_errors,
    resource_operations,
    resource_read_total,
    resource_update_total,
    schema_cache_hits,
    schema_generation_duration,
)


class TestMetricsImport:
    """Test that all metrics are importable and have correct types."""

    def test_all_metrics_importable(self) -> None:
        """Verify all metrics can be imported from observability module."""
        # Counter metrics
        assert resource_operations is not None
        assert resource_create_total is not None
        assert resource_read_total is not None
        assert resource_update_total is not None
        assert resource_delete_total is not None
        assert resource_errors is not None

        # Handler metrics
        assert handler_requests is not None
        assert handler_errors is not None

        # Discovery metrics
        assert components_discovered is not None
        assert discovery_errors is not None

        # Schema metrics
        assert schema_cache_hits is not None

        # Data source metrics
        assert datasource_read_total is not None
        assert datasource_errors is not None

        # Function metrics
        assert function_calls is not None
        assert function_errors is not None

        # Ephemeral metrics
        assert ephemeral_open_total is not None
        assert ephemeral_renew_total is not None
        assert ephemeral_close_total is not None
        assert ephemeral_errors is not None

        # Provider metrics
        assert provider_configure_total is not None
        assert provider_configure_errors is not None

        # Histogram metrics
        assert handler_duration is not None
        assert discovery_duration is not None
        assert schema_generation_duration is not None
        assert function_duration is not None

    def test_metrics_have_names(self) -> None:
        """Verify all metrics have name attributes."""
        assert hasattr(resource_operations, "name")
        assert hasattr(handler_duration, "name")
        assert hasattr(discovery_duration, "name")


class TestCounterMetrics:
    """Test counter metric functionality."""

    def test_resource_operations_counter(self) -> None:
        """Test resource_operations counter increments correctly."""
        initial_value = resource_operations.value
        resource_operations.inc(operation="create", resource_type="test")
        assert resource_operations.value == initial_value + 1

    def test_resource_create_counter(self) -> None:
        """Test resource_create_total counter."""
        initial_value = resource_create_total.value
        resource_create_total.inc(resource_type="aws_instance")
        assert resource_create_total.value == initial_value + 1

    def test_resource_read_counter(self) -> None:
        """Test resource_read_total counter."""
        initial_value = resource_read_total.value
        resource_read_total.inc(resource_type="aws_instance")
        assert resource_read_total.value == initial_value + 1

    def test_resource_update_counter(self) -> None:
        """Test resource_update_total counter."""
        initial_value = resource_update_total.value
        resource_update_total.inc(resource_type="aws_instance")
        assert resource_update_total.value == initial_value + 1

    def test_resource_delete_counter(self) -> None:
        """Test resource_delete_total counter."""
        initial_value = resource_delete_total.value
        resource_delete_total.inc(resource_type="aws_instance")
        assert resource_delete_total.value == initial_value + 1

    def test_resource_errors_counter(self) -> None:
        """Test resource_errors counter."""
        initial_value = resource_errors.value
        resource_errors.inc(operation="create", error_type="ValidationError")
        assert resource_errors.value == initial_value + 1

    def test_handler_requests_counter(self) -> None:
        """Test handler_requests counter."""
        initial_value = handler_requests.value
        handler_requests.inc(handler="ApplyResourceChange")
        assert handler_requests.value == initial_value + 1

    def test_handler_errors_counter(self) -> None:
        """Test handler_errors counter."""
        initial_value = handler_errors.value
        handler_errors.inc(handler="ApplyResourceChange", error="RuntimeError")
        assert handler_errors.value == initial_value + 1

    def test_components_discovered_counter(self) -> None:
        """Test components_discovered counter."""
        initial_value = components_discovered.value
        components_discovered.inc(component_type="resource")
        assert components_discovered.value == initial_value + 1

    def test_discovery_errors_counter(self) -> None:
        """Test discovery_errors counter."""
        initial_value = discovery_errors.value
        discovery_errors.inc(error_type="ImportError")
        assert discovery_errors.value == initial_value + 1

    def test_schema_cache_hits_counter(self) -> None:
        """Test schema_cache_hits counter."""
        initial_value = schema_cache_hits.value
        schema_cache_hits.inc()
        assert schema_cache_hits.value == initial_value + 1

    def test_datasource_read_counter(self) -> None:
        """Test datasource_read_total counter."""
        initial_value = datasource_read_total.value
        datasource_read_total.inc(datasource_type="aws_ami")
        assert datasource_read_total.value == initial_value + 1

    def test_datasource_errors_counter(self) -> None:
        """Test datasource_errors counter."""
        initial_value = datasource_errors.value
        datasource_errors.inc(datasource_type="aws_ami", error="NotFoundError")
        assert datasource_errors.value == initial_value + 1

    def test_function_calls_counter(self) -> None:
        """Test function_calls counter."""
        initial_value = function_calls.value
        function_calls.inc(function_name="test_function")
        assert function_calls.value == initial_value + 1

    def test_function_errors_counter(self) -> None:
        """Test function_errors counter."""
        initial_value = function_errors.value
        function_errors.inc(function_name="test_function", error="ValueError")
        assert function_errors.value == initial_value + 1

    def test_ephemeral_open_counter(self) -> None:
        """Test ephemeral_open_total counter."""
        initial_value = ephemeral_open_total.value
        ephemeral_open_total.inc(ephemeral_type="aws_credentials")
        assert ephemeral_open_total.value == initial_value + 1

    def test_ephemeral_renew_counter(self) -> None:
        """Test ephemeral_renew_total counter."""
        initial_value = ephemeral_renew_total.value
        ephemeral_renew_total.inc(ephemeral_type="aws_credentials")
        assert ephemeral_renew_total.value == initial_value + 1

    def test_ephemeral_close_counter(self) -> None:
        """Test ephemeral_close_total counter."""
        initial_value = ephemeral_close_total.value
        ephemeral_close_total.inc(ephemeral_type="aws_credentials")
        assert ephemeral_close_total.value == initial_value + 1

    def test_ephemeral_errors_counter(self) -> None:
        """Test ephemeral_errors counter."""
        initial_value = ephemeral_errors.value
        ephemeral_errors.inc(ephemeral_type="aws_credentials", operation="open")
        assert ephemeral_errors.value == initial_value + 1

    def test_provider_configure_counter(self) -> None:
        """Test provider_configure_total counter."""
        initial_value = provider_configure_total.value
        provider_configure_total.inc()
        assert provider_configure_total.value == initial_value + 1

    def test_provider_configure_errors_counter(self) -> None:
        """Test provider_configure_errors counter."""
        initial_value = provider_configure_errors.value
        provider_configure_errors.inc(error="ConfigurationError")
        assert provider_configure_errors.value == initial_value + 1


class TestHistogramMetrics:
    """Test histogram metric functionality."""

    def test_handler_duration_histogram(self) -> None:
        """Test handler_duration histogram records observations."""
        initial_count = handler_duration.count
        handler_duration.observe(0.123, handler="ApplyResourceChange")
        assert handler_duration.count == initial_count + 1

    def test_handler_duration_multiple_observations(self) -> None:
        """Test handler_duration with multiple observations."""
        initial_count = handler_duration.count
        handler_duration.observe(0.1, handler="PlanResourceChange")
        handler_duration.observe(0.2, handler="PlanResourceChange")
        handler_duration.observe(0.3, handler="PlanResourceChange")
        assert handler_duration.count == initial_count + 3

    def test_discovery_duration_histogram(self) -> None:
        """Test discovery_duration histogram."""
        initial_count = discovery_duration.count
        discovery_duration.observe(1.5, phase="component_discovery")
        assert discovery_duration.count == initial_count + 1

    def test_schema_generation_duration_histogram(self) -> None:
        """Test schema_generation_duration histogram."""
        initial_count = schema_generation_duration.count
        schema_generation_duration.observe(0.05, schema_type="resource")
        assert schema_generation_duration.count == initial_count + 1

    def test_function_duration_histogram(self) -> None:
        """Test function_duration histogram."""
        initial_count = function_duration.count
        function_duration.observe(0.01, function_name="test_function")
        assert function_duration.count == initial_count + 1


class TestMetricsWithLabels:
    """Test metrics with various label combinations."""

    def test_counter_with_no_labels(self) -> None:
        """Test counter increments without labels."""
        initial_value = schema_cache_hits.value
        schema_cache_hits.inc()
        assert schema_cache_hits.value == initial_value + 1

    def test_counter_with_single_label(self) -> None:
        """Test counter increments with single label."""
        initial_value = resource_create_total.value
        resource_create_total.inc(resource_type="test")
        assert resource_create_total.value == initial_value + 1

    def test_counter_with_multiple_labels(self) -> None:
        """Test counter increments with multiple labels."""
        initial_value = resource_errors.value
        resource_errors.inc(operation="create", error_type="ValidationError", resource="test")
        assert resource_errors.value == initial_value + 1

    def test_histogram_with_labels(self) -> None:
        """Test histogram observations with labels."""
        initial_count = handler_duration.count
        handler_duration.observe(0.5, handler="Test", method="POST")
        assert handler_duration.count == initial_count + 1

    def test_counter_increments_by_custom_value(self) -> None:
        """Test counter can increment by values other than 1."""
        initial_value = resource_operations.value
        resource_operations.inc(5, operation="bulk_create")
        assert resource_operations.value == initial_value + 5


class TestMetricsIntegration:
    """Integration tests for metrics in realistic scenarios."""

    def test_resource_lifecycle_metrics(self) -> None:
        """Test complete resource lifecycle metrics."""
        # Create
        create_initial = resource_create_total.value
        resource_create_total.inc(resource_type="test_resource")
        assert resource_create_total.value == create_initial + 1

        # Read
        read_initial = resource_read_total.value
        resource_read_total.inc(resource_type="test_resource")
        assert resource_read_total.value == read_initial + 1

        # Update
        update_initial = resource_update_total.value
        resource_update_total.inc(resource_type="test_resource")
        assert resource_update_total.value == update_initial + 1

        # Delete
        delete_initial = resource_delete_total.value
        resource_delete_total.inc(resource_type="test_resource")
        assert resource_delete_total.value == delete_initial + 1

    def test_handler_success_flow(self) -> None:
        """Test handler metrics for successful request."""
        requests_initial = handler_requests.value
        duration_initial = handler_duration.count

        # Simulate successful handler
        handler_requests.inc(handler="TestHandler")
        handler_duration.observe(0.123, handler="TestHandler")

        assert handler_requests.value == requests_initial + 1
        assert handler_duration.count == duration_initial + 1

    def test_handler_error_flow(self) -> None:
        """Test handler metrics for failed request."""
        requests_initial = handler_requests.value
        errors_initial = handler_errors.value
        duration_initial = handler_duration.count

        # Simulate failed handler
        handler_requests.inc(handler="TestHandler")
        handler_errors.inc(handler="TestHandler", error="RuntimeError")
        handler_duration.observe(0.05, handler="TestHandler")

        assert handler_requests.value == requests_initial + 1
        assert handler_errors.value == errors_initial + 1
        assert handler_duration.count == duration_initial + 1

    def test_ephemeral_resource_lifecycle(self) -> None:
        """Test ephemeral resource lifecycle metrics."""
        open_initial = ephemeral_open_total.value
        renew_initial = ephemeral_renew_total.value
        close_initial = ephemeral_close_total.value

        ephemeral_open_total.inc(ephemeral_type="credentials")
        ephemeral_renew_total.inc(ephemeral_type="credentials")
        ephemeral_close_total.inc(ephemeral_type="credentials")

        assert ephemeral_open_total.value == open_initial + 1
        assert ephemeral_renew_total.value == renew_initial + 1
        assert ephemeral_close_total.value == close_initial + 1


# 🐍🏗️🔚
