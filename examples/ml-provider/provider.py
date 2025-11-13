"""
Machine Learning Provider for Pyvider

This provider demonstrates managing machine learning workflows as infrastructure,
including models, datasets, experiments, and training jobs.

Novel aspects:
- ML lifecycle management through Terraform
- Experiment tracking and versioning
- Model registry as infrastructure
- Declarative ML pipeline configuration
- Reproducible ML workflows
"""

from __future__ import annotations

import hashlib
import json
import math
import random
from datetime import datetime
from typing import Any

from attrs import define, field
from pyvider.data_sources import BaseDataSource, register_data_source
from pyvider.functions import BaseFunction, register_function
from pyvider.providers import BaseProvider, register_provider
from pyvider.resources import BaseResource, register_resource
from pyvider.schema import (
    PvsSchema,
    a_bool,
    a_float,
    a_list,
    a_map,
    a_num,
    a_str,
    s_block,
    s_data_source,
    s_function,
    s_provider,
    s_resource,
)


# ============================================================================
# Provider
# ============================================================================


@register_provider()
class MLProvider(BaseProvider):
    """Machine Learning infrastructure provider."""

    @define
    class Config:
        """Provider configuration."""

        experiment_tracking_uri: str = field(default="file:///tmp/mlruns")
        model_registry_uri: str = field(default="file:///tmp/models")
        default_framework: str = field(default="pytorch")
        enable_gpu: bool = field(default=False)
        random_seed: int = field(default=42)

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_provider(
            {
                "experiment_tracking_uri": a_str(
                    optional=True,
                    description="URI for experiment tracking (e.g., MLflow tracking server)",
                ),
                "model_registry_uri": a_str(
                    optional=True,
                    description="URI for model registry storage",
                ),
                "default_framework": a_str(
                    optional=True,
                    description="Default ML framework (pytorch, tensorflow, sklearn)",
                ),
                "enable_gpu": a_bool(
                    optional=True,
                    description="Enable GPU acceleration for training",
                ),
                "random_seed": a_num(
                    optional=True,
                    description="Random seed for reproducibility",
                ),
            }
        )

    async def configure(self, config: Config) -> None:
        """Configure the ML provider."""
        self.config = config
        # In real implementation, would initialize MLflow client, etc.


# ============================================================================
# Resources
# ============================================================================


@register_resource("dataset")
class MLDataset(BaseResource):
    """Machine learning dataset with versioning and validation."""

    @define
    class Config:
        """Dataset configuration."""

        name: str
        source_uri: str
        version: str = field(default="1.0.0")
        format: str = field(default="csv")
        schema: dict[str, str] = field(factory=dict)
        split_ratios: dict[str, float] = field(factory=dict)
        preprocessing: list[str] = field(factory=list)
        validation_rules: dict[str, str] = field(factory=dict)
        tags: dict[str, str] = field(factory=dict)

    @define
    class State:
        """Dataset state."""

        name: str
        source_uri: str
        version: str
        format: str
        schema: dict[str, str]
        split_ratios: dict[str, float]
        preprocessing: list[str]
        validation_rules: dict[str, str]
        tags: dict[str, str]
        # Computed
        dataset_id: str = ""
        row_count: int = 0
        column_count: int = 0
        size_bytes: int = 0
        checksum: str = ""
        train_rows: int = 0
        val_rows: int = 0
        test_rows: int = 0
        created_at: str = ""
        status: str = "ready"

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            {
                "name": a_str(required=True, description="Dataset name"),
                "source_uri": a_str(required=True, description="Data source URI"),
                "version": a_str(optional=True, description="Dataset version"),
                "format": a_str(optional=True, description="Data format (csv, parquet, json)"),
                "schema": a_map(
                    a_str(),
                    optional=True,
                    description="Column schema (name -> type)",
                ),
                "split_ratios": a_map(
                    a_float(),
                    optional=True,
                    description="Train/val/test split ratios",
                ),
                "preprocessing": a_list(
                    a_str(),
                    optional=True,
                    description="Preprocessing steps to apply",
                ),
                "validation_rules": a_map(
                    a_str(),
                    optional=True,
                    description="Data validation rules",
                ),
                "tags": a_map(a_str(), optional=True, description="Dataset tags"),
                # Computed
                "dataset_id": a_str(computed=True, description="Unique dataset ID"),
                "row_count": a_num(computed=True, description="Total number of rows"),
                "column_count": a_num(computed=True, description="Number of columns"),
                "size_bytes": a_num(computed=True, description="Dataset size in bytes"),
                "checksum": a_str(computed=True, description="Data checksum for versioning"),
                "train_rows": a_num(computed=True, description="Training set row count"),
                "val_rows": a_num(computed=True, description="Validation set row count"),
                "test_rows": a_num(computed=True, description="Test set row count"),
                "created_at": a_str(computed=True, description="Creation timestamp"),
                "status": a_str(computed=True, description="Dataset status"),
            }
        )

    async def _create(self, ctx: Any, base_plan: dict) -> tuple[dict | None, bytes | None]:
        """Create dataset."""
        config = self.Config(**base_plan)

        # Generate dataset ID
        dataset_id = f"ds-{hashlib.md5(config.name.encode()).hexdigest()[:12]}"

        # Simulate loading and analyzing dataset
        # In real implementation, would actually load and process data
        row_count = random.randint(1000, 100000)
        column_count = len(config.schema) if config.schema else random.randint(5, 50)

        # Calculate split sizes
        split_ratios = config.split_ratios or {"train": 0.7, "val": 0.15, "test": 0.15}
        train_rows = int(row_count * split_ratios.get("train", 0.7))
        val_rows = int(row_count * split_ratios.get("val", 0.15))
        test_rows = row_count - train_rows - val_rows

        # Generate checksum
        checksum_data = f"{config.source_uri}-{config.version}-{row_count}"
        checksum = hashlib.sha256(checksum_data.encode()).hexdigest()[:16]

        state = {
            **base_plan,
            "dataset_id": dataset_id,
            "row_count": row_count,
            "column_count": column_count,
            "size_bytes": row_count * column_count * 8,  # Rough estimate
            "checksum": checksum,
            "train_rows": train_rows,
            "val_rows": val_rows,
            "test_rows": test_rows,
            "created_at": datetime.now().isoformat(),
            "status": "ready",
        }

        return state, None

    async def read(self, ctx: Any) -> State | None:
        """Read dataset state."""
        # In real implementation, would verify dataset still exists
        return self.State(**ctx.state.model_dump())

    async def _update(self, ctx: Any, base_plan: dict) -> tuple[dict | None, bytes | None]:
        """Update dataset (e.g., new version)."""
        # Regenerate checksum for new version
        config = self.Config(**base_plan)
        checksum_data = f"{config.source_uri}-{config.version}-{ctx.state.row_count}"
        new_checksum = hashlib.sha256(checksum_data.encode()).hexdigest()[:16]

        updated_state = {
            **base_plan,
            "dataset_id": ctx.state.dataset_id,
            "row_count": ctx.state.row_count,
            "column_count": ctx.state.column_count,
            "size_bytes": ctx.state.size_bytes,
            "checksum": new_checksum,
            "train_rows": ctx.state.train_rows,
            "val_rows": ctx.state.val_rows,
            "test_rows": ctx.state.test_rows,
            "created_at": ctx.state.created_at,
            "status": "ready",
        }

        return updated_state, None

    async def _delete(self, ctx: Any) -> None:
        """Delete dataset."""
        # In real implementation, would remove dataset files
        pass


@register_resource("model")
class MLModel(BaseResource):
    """Machine learning model with versioning and metadata."""

    @define
    class Config:
        """Model configuration."""

        name: str
        framework: str
        architecture: str
        version: str = field(default="1.0.0")
        hyperparameters: dict[str, Any] = field(factory=dict)
        input_schema: dict[str, str] = field(factory=dict)
        output_schema: dict[str, str] = field(factory=dict)
        pretrained_weights: str = field(default="")
        tags: dict[str, str] = field(factory=dict)

    @define
    class State:
        """Model state."""

        name: str
        framework: str
        architecture: str
        version: str
        hyperparameters: dict[str, Any]
        input_schema: dict[str, str]
        output_schema: dict[str, str]
        pretrained_weights: str
        tags: dict[str, str]
        # Computed
        model_id: str = ""
        parameter_count: int = 0
        size_bytes: int = 0
        model_uri: str = ""
        checksum: str = ""
        created_at: str = ""
        status: str = "initialized"

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            {
                "name": a_str(required=True, description="Model name"),
                "framework": a_str(
                    required=True,
                    description="ML framework (pytorch, tensorflow, sklearn)",
                ),
                "architecture": a_str(required=True, description="Model architecture"),
                "version": a_str(optional=True, description="Model version"),
                "hyperparameters": a_map(
                    a_str(),
                    optional=True,
                    description="Model hyperparameters (as JSON strings)",
                ),
                "input_schema": a_map(
                    a_str(),
                    optional=True,
                    description="Input tensor/feature schema",
                ),
                "output_schema": a_map(
                    a_str(),
                    optional=True,
                    description="Output schema",
                ),
                "pretrained_weights": a_str(
                    optional=True,
                    description="URI to pretrained weights",
                ),
                "tags": a_map(a_str(), optional=True, description="Model tags"),
                # Computed
                "model_id": a_str(computed=True, description="Unique model ID"),
                "parameter_count": a_num(computed=True, description="Number of parameters"),
                "size_bytes": a_num(computed=True, description="Model size in bytes"),
                "model_uri": a_str(computed=True, description="Model storage URI"),
                "checksum": a_str(computed=True, description="Model weights checksum"),
                "created_at": a_str(computed=True, description="Creation timestamp"),
                "status": a_str(computed=True, description="Model status"),
            }
        )

    async def _create(self, ctx: Any, base_plan: dict) -> tuple[dict | None, bytes | None]:
        """Create model."""
        config = self.Config(**base_plan)

        # Generate model ID
        model_id = f"model-{hashlib.md5(config.name.encode()).hexdigest()[:12]}"

        # Estimate parameter count based on architecture
        param_count = self._estimate_parameters(config.architecture)

        # Generate model URI
        model_uri = f"models://{config.name}/{config.version}"

        # Generate checksum
        checksum_data = f"{config.name}-{config.architecture}-{config.version}"
        checksum = hashlib.sha256(checksum_data.encode()).hexdigest()[:16]

        state = {
            **base_plan,
            "model_id": model_id,
            "parameter_count": param_count,
            "size_bytes": param_count * 4,  # 4 bytes per float32 parameter
            "model_uri": model_uri,
            "checksum": checksum,
            "created_at": datetime.now().isoformat(),
            "status": "initialized",
        }

        return state, None

    def _estimate_parameters(self, architecture: str) -> int:
        """Estimate parameter count based on architecture name."""
        # Simple heuristic - in real implementation would be more sophisticated
        if "tiny" in architecture.lower():
            return random.randint(1_000_000, 5_000_000)
        elif "small" in architecture.lower():
            return random.randint(5_000_000, 50_000_000)
        elif "base" in architecture.lower():
            return random.randint(50_000_000, 200_000_000)
        elif "large" in architecture.lower():
            return random.randint(200_000_000, 1_000_000_000)
        else:
            return random.randint(10_000_000, 100_000_000)

    async def read(self, ctx: Any) -> State | None:
        """Read model state."""
        return self.State(**ctx.state.model_dump())

    async def _update(self, ctx: Any, base_plan: dict) -> tuple[dict | None, bytes | None]:
        """Update model (new version)."""
        config = self.Config(**base_plan)
        checksum_data = f"{config.name}-{config.architecture}-{config.version}"
        new_checksum = hashlib.sha256(checksum_data.encode()).hexdigest()[:16]

        updated_state = {
            **base_plan,
            "model_id": ctx.state.model_id,
            "parameter_count": ctx.state.parameter_count,
            "size_bytes": ctx.state.size_bytes,
            "model_uri": f"models://{config.name}/{config.version}",
            "checksum": new_checksum,
            "created_at": ctx.state.created_at,
            "status": "updated",
        }

        return updated_state, None

    async def _delete(self, ctx: Any) -> None:
        """Delete model."""
        pass


@register_resource("training_job")
class TrainingJob(BaseResource):
    """Machine learning training job with experiment tracking."""

    @define
    class Config:
        """Training job configuration."""

        name: str
        model_id: str
        dataset_id: str
        epochs: int = field(default=10)
        batch_size: int = field(default=32)
        learning_rate: float = field(default=0.001)
        optimizer: str = field(default="adam")
        loss_function: str = field(default="cross_entropy")
        metrics: list[str] = field(factory=list)
        early_stopping: bool = field(default=True)
        patience: int = field(default=5)
        checkpoint_frequency: int = field(default=1)
        distributed: bool = field(default=False)
        num_gpus: int = field(default=1)
        tags: dict[str, str] = field(factory=dict)

    @define
    class State:
        """Training job state."""

        name: str
        model_id: str
        dataset_id: str
        epochs: int
        batch_size: int
        learning_rate: float
        optimizer: str
        loss_function: str
        metrics: list[str]
        early_stopping: bool
        patience: int
        checkpoint_frequency: int
        distributed: bool
        num_gpus: int
        tags: dict[str, str]
        # Computed
        job_id: str = ""
        experiment_id: str = ""
        run_id: str = ""
        status: str = "pending"
        current_epoch: int = 0
        best_epoch: int = 0
        train_loss: float = 0.0
        val_loss: float = 0.0
        best_val_loss: float = float("inf")
        train_accuracy: float = 0.0
        val_accuracy: float = 0.0
        best_val_accuracy: float = 0.0
        training_time_seconds: int = 0
        checkpoint_uri: str = ""
        logs_uri: str = ""
        started_at: str = ""
        completed_at: str = ""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            {
                "name": a_str(required=True, description="Training job name"),
                "model_id": a_str(required=True, description="Model ID to train"),
                "dataset_id": a_str(required=True, description="Dataset ID for training"),
                "epochs": a_num(optional=True, description="Number of training epochs"),
                "batch_size": a_num(optional=True, description="Batch size"),
                "learning_rate": a_float(optional=True, description="Learning rate"),
                "optimizer": a_str(optional=True, description="Optimizer (adam, sgd, etc.)"),
                "loss_function": a_str(optional=True, description="Loss function"),
                "metrics": a_list(a_str(), optional=True, description="Metrics to track"),
                "early_stopping": a_bool(optional=True, description="Enable early stopping"),
                "patience": a_num(optional=True, description="Early stopping patience"),
                "checkpoint_frequency": a_num(
                    optional=True,
                    description="Save checkpoint every N epochs",
                ),
                "distributed": a_bool(optional=True, description="Use distributed training"),
                "num_gpus": a_num(optional=True, description="Number of GPUs to use"),
                "tags": a_map(a_str(), optional=True, description="Job tags"),
                # Computed
                "job_id": a_str(computed=True, description="Unique job ID"),
                "experiment_id": a_str(computed=True, description="MLflow experiment ID"),
                "run_id": a_str(computed=True, description="MLflow run ID"),
                "status": a_str(computed=True, description="Job status"),
                "current_epoch": a_num(computed=True, description="Current epoch number"),
                "best_epoch": a_num(computed=True, description="Best performing epoch"),
                "train_loss": a_float(computed=True, description="Current training loss"),
                "val_loss": a_float(computed=True, description="Current validation loss"),
                "best_val_loss": a_float(computed=True, description="Best validation loss"),
                "train_accuracy": a_float(computed=True, description="Training accuracy"),
                "val_accuracy": a_float(computed=True, description="Validation accuracy"),
                "best_val_accuracy": a_float(
                    computed=True,
                    description="Best validation accuracy",
                ),
                "training_time_seconds": a_num(
                    computed=True,
                    description="Total training time",
                ),
                "checkpoint_uri": a_str(computed=True, description="Best checkpoint URI"),
                "logs_uri": a_str(computed=True, description="Training logs URI"),
                "started_at": a_str(computed=True, description="Job start time"),
                "completed_at": a_str(computed=True, description="Job completion time"),
            }
        )

    async def _create(self, ctx: Any, base_plan: dict) -> tuple[dict | None, bytes | None]:
        """Create and start training job."""
        config = self.Config(**base_plan)

        # Generate IDs
        job_id = f"job-{hashlib.md5(config.name.encode()).hexdigest()[:12]}"
        experiment_id = f"exp-{hashlib.md5(config.model_id.encode()).hexdigest()[:8]}"
        run_id = f"run-{hashlib.md5(job_id.encode()).hexdigest()[:8]}"

        # Simulate training completion with results
        # In real implementation, would actually submit training job
        final_epoch = config.epochs
        best_epoch = random.randint(config.epochs // 2, config.epochs)

        # Simulate learning curves
        best_val_loss = random.uniform(0.1, 0.5)
        best_val_accuracy = random.uniform(0.85, 0.98)

        state = {
            **base_plan,
            "job_id": job_id,
            "experiment_id": experiment_id,
            "run_id": run_id,
            "status": "completed",
            "current_epoch": final_epoch,
            "best_epoch": best_epoch,
            "train_loss": best_val_loss * 0.8,
            "val_loss": best_val_loss,
            "best_val_loss": best_val_loss,
            "train_accuracy": best_val_accuracy + 0.02,
            "val_accuracy": best_val_accuracy,
            "best_val_accuracy": best_val_accuracy,
            "training_time_seconds": config.epochs * 120,  # ~2 min per epoch
            "checkpoint_uri": f"s3://models/{config.model_id}/checkpoints/epoch-{best_epoch}",
            "logs_uri": f"s3://logs/{job_id}/",
            "started_at": datetime.now().isoformat(),
            "completed_at": datetime.now().isoformat(),
        }

        return state, None

    async def read(self, ctx: Any) -> State | None:
        """Read training job state."""
        return self.State(**ctx.state.model_dump())

    async def _update(self, ctx: Any, base_plan: dict) -> tuple[dict | None, bytes | None]:
        """Update training job (restart with new config)."""
        # Rerun training
        return await self._create(ctx, base_plan)

    async def _delete(self, ctx: Any) -> None:
        """Delete training job (stop if running)."""
        pass


# ============================================================================
# Data Sources
# ============================================================================


@register_data_source("experiment_metrics")
class ExperimentMetrics(BaseDataSource):
    """Query metrics from ML experiments."""

    @define
    class Config:
        """Data source configuration."""

        experiment_id: str = field(default="")
        metric_names: list[str] = field(factory=list)
        filter_tags: dict[str, str] = field(factory=dict)

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_data_source(
            {
                "experiment_id": a_str(
                    optional=True,
                    description="Filter by experiment ID",
                ),
                "metric_names": a_list(
                    a_str(),
                    optional=True,
                    description="Metrics to retrieve",
                ),
                "filter_tags": a_map(
                    a_str(),
                    optional=True,
                    description="Filter by tags",
                ),
                # Computed
                "id": a_str(computed=True, description="Query ID"),
                "runs": a_list(
                    s_block(
                        {
                            "run_id": a_str(description="Run ID"),
                            "metrics": a_map(a_float(), description="Metric values"),
                            "status": a_str(description="Run status"),
                            "duration_seconds": a_num(description="Run duration"),
                        }
                    ),
                    computed=True,
                    description="Experiment runs with metrics",
                ),
                "best_run_id": a_str(computed=True, description="Best performing run ID"),
                "best_metric_value": a_float(
                    computed=True,
                    description="Best metric value",
                ),
            }
        )

    async def read(self, ctx: Any) -> dict[str, Any]:
        """Read experiment metrics."""
        config = self.Config(**ctx.config.model_dump())

        # Simulate querying experiment runs
        # In real implementation, would query MLflow or similar
        runs = []
        best_value = 0.0
        best_run = ""

        for i in range(5):
            run_id = f"run-{i:03d}"
            accuracy = random.uniform(0.80, 0.95)
            loss = random.uniform(0.1, 0.5)

            if accuracy > best_value:
                best_value = accuracy
                best_run = run_id

            runs.append(
                {
                    "run_id": run_id,
                    "metrics": {
                        "accuracy": accuracy,
                        "loss": loss,
                        "f1_score": random.uniform(0.75, 0.92),
                    },
                    "status": "completed",
                    "duration_seconds": random.randint(300, 3600),
                }
            )

        return {
            "id": f"query-{hashlib.md5(config.experiment_id.encode()).hexdigest()[:8]}",
            "runs": runs,
            "best_run_id": best_run,
            "best_metric_value": best_value,
        }


@register_data_source("model_registry")
class ModelRegistry(BaseDataSource):
    """Query model registry for deployed models."""

    @define
    class Config:
        """Data source configuration."""

        filter_framework: str = field(default="")
        filter_stage: str = field(default="")
        min_accuracy: float = field(default=0.0)

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_data_source(
            {
                "filter_framework": a_str(
                    optional=True,
                    description="Filter by framework",
                ),
                "filter_stage": a_str(
                    optional=True,
                    description="Filter by stage (staging, production)",
                ),
                "min_accuracy": a_float(
                    optional=True,
                    description="Minimum accuracy threshold",
                ),
                # Computed
                "id": a_str(computed=True, description="Query ID"),
                "models": a_list(
                    s_block(
                        {
                            "model_id": a_str(description="Model ID"),
                            "name": a_str(description="Model name"),
                            "version": a_str(description="Model version"),
                            "framework": a_str(description="ML framework"),
                            "stage": a_str(description="Deployment stage"),
                            "accuracy": a_float(description="Model accuracy"),
                            "created_at": a_str(description="Creation timestamp"),
                        }
                    ),
                    computed=True,
                    description="Registered models",
                ),
                "count": a_num(computed=True, description="Number of models found"),
            }
        )

    async def read(self, ctx: Any) -> dict[str, Any]:
        """Read model registry."""
        config = self.Config(**ctx.config.model_dump())

        # Simulate querying model registry
        models = []
        frameworks = ["pytorch", "tensorflow", "sklearn"]
        stages = ["staging", "production"]

        for i in range(3):
            framework = random.choice(frameworks)
            stage = random.choice(stages)
            accuracy = random.uniform(0.85, 0.98)

            # Apply filters
            if config.filter_framework and framework != config.filter_framework:
                continue
            if config.filter_stage and stage != config.filter_stage:
                continue
            if accuracy < config.min_accuracy:
                continue

            models.append(
                {
                    "model_id": f"model-{i:03d}",
                    "name": f"classifier-{framework}-{i}",
                    "version": f"1.{i}.0",
                    "framework": framework,
                    "stage": stage,
                    "accuracy": accuracy,
                    "created_at": datetime.now().isoformat(),
                }
            )

        return {
            "id": f"registry-query-{random.randint(1000, 9999)}",
            "models": models,
            "count": len(models),
        }


# ============================================================================
# Functions
# ============================================================================


@register_function("calculate_metrics")
class CalculateMetrics(BaseFunction):
    """Calculate ML evaluation metrics."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_function(
            {
                "predictions": a_list(a_float(), description="Model predictions"),
                "labels": a_list(a_float(), description="True labels"),
                "metric": a_str(description="Metric to calculate (accuracy, f1, etc.)"),
            },
            a_float(description="Calculated metric value"),
        )

    async def call(
        self,
        predictions: list[float],
        labels: list[float],
        metric: str,
    ) -> float:
        """Calculate specified metric."""
        if len(predictions) != len(labels):
            raise ValueError("Predictions and labels must have same length")

        if metric == "accuracy":
            correct = sum(1 for p, l in zip(predictions, labels) if round(p) == round(l))
            return correct / len(labels)

        elif metric == "mse":
            return sum((p - l) ** 2 for p, l in zip(predictions, labels)) / len(labels)

        elif metric == "mae":
            return sum(abs(p - l) for p, l in zip(predictions, labels)) / len(labels)

        elif metric == "rmse":
            mse = sum((p - l) ** 2 for p, l in zip(predictions, labels)) / len(labels)
            return math.sqrt(mse)

        else:
            raise ValueError(f"Unknown metric: {metric}")


@register_function("split_dataset")
class SplitDataset(BaseFunction):
    """Calculate dataset split sizes."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_function(
            {
                "total_size": a_num(description="Total dataset size"),
                "train_ratio": a_float(description="Training set ratio"),
                "val_ratio": a_float(description="Validation set ratio"),
                "test_ratio": a_float(description="Test set ratio"),
            },
            a_map(a_num(), description="Split sizes (train, val, test)"),
        )

    async def call(
        self,
        total_size: float,
        train_ratio: float,
        val_ratio: float,
        test_ratio: float,
    ) -> dict[str, float]:
        """Calculate split sizes."""
        # Validate ratios sum to 1.0
        total_ratio = train_ratio + val_ratio + test_ratio
        if not math.isclose(total_ratio, 1.0, abs_tol=0.001):
            raise ValueError(f"Ratios must sum to 1.0, got {total_ratio}")

        train_size = int(total_size * train_ratio)
        val_size = int(total_size * val_ratio)
        test_size = int(total_size) - train_size - val_size

        return {
            "train": float(train_size),
            "val": float(val_size),
            "test": float(test_size),
        }


@register_function("estimate_training_time")
class EstimateTrainingTime(BaseFunction):
    """Estimate training time based on dataset and model size."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_function(
            {
                "dataset_rows": a_num(description="Number of training samples"),
                "model_parameters": a_num(description="Number of model parameters"),
                "batch_size": a_num(description="Batch size"),
                "epochs": a_num(description="Number of epochs"),
                "gpu_enabled": a_bool(description="Whether GPU is enabled"),
            },
            a_num(description="Estimated training time in seconds"),
        )

    async def call(
        self,
        dataset_rows: float,
        model_parameters: float,
        batch_size: float,
        epochs: float,
        gpu_enabled: bool,
    ) -> float:
        """Estimate training time."""
        # Simplified estimation formula
        batches_per_epoch = math.ceil(dataset_rows / batch_size)
        seconds_per_batch = (model_parameters / 1_000_000) * 0.01  # Base time

        # GPU speedup
        if gpu_enabled:
            seconds_per_batch /= 10

        total_seconds = batches_per_epoch * seconds_per_batch * epochs

        return total_seconds


@register_function("generate_model_name")
class GenerateModelName(BaseFunction):
    """Generate standardized model names."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_function(
            {
                "task": a_str(description="ML task (classification, regression, etc.)"),
                "framework": a_str(description="Framework name"),
                "architecture": a_str(description="Architecture name"),
                "version": a_str(description="Version string"),
            },
            a_str(description="Generated model name"),
        )

    async def call(
        self,
        task: str,
        framework: str,
        architecture: str,
        version: str,
    ) -> str:
        """Generate model name."""
        # Format: task-framework-architecture-version
        # Example: classification-pytorch-resnet50-v1.0
        task_clean = task.lower().replace(" ", "-")
        framework_clean = framework.lower()
        arch_clean = architecture.lower().replace(" ", "-")

        return f"{task_clean}-{framework_clean}-{arch_clean}-{version}"
