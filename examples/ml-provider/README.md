# Machine Learning Provider - Pyvider Example

A **novel** Terraform provider that treats machine learning workflows as infrastructure-as-code. This provider demonstrates that ML operations—datasets, models, experiments, and training jobs—can be managed declaratively using Terraform.

## Why This Is Unique

Traditional ML platforms (MLflow, Kubeflow, SageMaker) use imperative APIs or custom UIs. This provider demonstrates that **ML workflows are infrastructure** and should be:

- **Declarative**: Define desired ML state, not procedural steps
- **Versioned**: Track ML infrastructure changes in git
- **Reproducible**: Identical config produces identical results
- **Auditable**: Full history of ML experiments and models
- **Collaborative**: Team workflows through pull requests

## Novel Aspects

### 1. ML Lifecycle as Infrastructure

```hcl
# Dataset is a versioned resource
resource "ml_dataset" "training_data" {
  name    = "imagenet-v1"
  version = "1.0.0"
  # Changes trigger new dataset version
}

# Model is infrastructure
resource "ml_model" "classifier" {
  architecture = "resnet50"
  version      = "2.0.0"
  # Model evolution tracked in git
}

# Training is a declarative operation
resource "ml_training_job" "experiment" {
  model_id   = ml_model.classifier.id
  dataset_id = ml_dataset.training_data.id
  epochs     = 50
  # Reproducible experiments
}
```

### 2. Experiment Tracking via Data Sources

```hcl
# Query experiment results
data "ml_experiment_metrics" "results" {
  experiment_id = ml_training_job.experiment.id
  metric_names  = ["accuracy", "loss"]
}

# Use in deployment decisions
output "deploy_model" {
  value = data.ml_experiment_metrics.results.best_metric_value > 0.95
}
```

### 3. ML Functions for Calculations

```hcl
locals {
  # Calculate dataset splits
  splits = provider::ml::split_dataset(10000, 0.7, 0.15, 0.15)

  # Estimate training time
  hours = provider::ml::estimate_training_time(
    dataset_rows, model_params, batch_size, epochs, gpu_enabled
  ) / 3600

  # Calculate metrics
  accuracy = provider::ml::calculate_metrics(predictions, labels, "accuracy")
}
```

---

## Features Demonstrated

### Pyvider Capabilities

- **3 Resource Types**: Dataset (versioned data), Model (architectures), TrainingJob (experiments)
- **2 Data Sources**: ExperimentMetrics (results), ModelRegistry (deployed models)
- **4 Provider Functions**: Metrics calculation, split calculation, time estimation, name generation
- **Complex State**: Nested schemas, computed attributes, relationship management
- **Async Operations**: Training jobs as long-running async operations

### ML Workflow Features

- **Dataset Management**: Versioning, validation, preprocessing, split configuration
- **Model Versioning**: Architecture definitions, hyperparameters, weight checkpoints
- **Experiment Tracking**: Metrics, logs, checkpoints, reproducibility
- **Model Registry**: Staging/production promotion, model search
- **Cost Estimation**: Training time and cost predictions

---

## Quick Start

### 1. Install Dependencies

```bash
cd examples/ml-provider
pip install pyvider
```

Or using `uv`:
```bash
uv sync
```

### 2. Install the Provider

```bash
pyvider install
```

### 3. Initialize Terraform

```bash
terraform init
```

### 4. Apply Configuration

```bash
terraform plan
terraform apply
```

### 5. View ML Infrastructure

```bash
terraform output ml_infrastructure_summary
```

Example output:
```json
{
  "datasets": {
    "count": 3,
    "total_rows": 234567,
    "total_size_gb": 45.6
  },
  "models": {
    "count": 3,
    "total_parameters": 350000000,
    "frameworks": ["pytorch", "pytorch", "tensorflow"]
  },
  "training_jobs": {
    "count": 6,
    "total_epochs": 190,
    "total_gpus": 7
  },
  "cost_estimate": {
    "training_cost_usd": 42.50,
    "total_training_hours": 6.8
  }
}
```

---

## Example Scenarios

### 1. Versioned Dataset Management

Track dataset evolution and ensure reproducibility:

```hcl
resource "ml_dataset" "production_data" {
  name       = "user-behavior-v1"
  source_uri = "s3://data/users/2024-11/"
  version    = "1.0.0"  # Git tag: data-v1.0.0

  schema = {
    user_id    = "string"
    action     = "string"
    timestamp  = "datetime"
  }

  split_ratios = {
    train = 0.7
    val   = 0.15
    test  = 0.15
  }

  validation_rules = {
    no_duplicates = "unique(user_id, timestamp)"
    no_nulls      = "required(action)"
  }
}

# Later: Update to new data version
# Change source_uri and version, commit to git
# Full audit trail of data changes
```

**Why This Matters**:
- Dataset changes tracked in version control
- Reproducible experiments (same dataset version = same results)
- Audit trail for compliance (what data was used when?)
- Rollback capability if data issues discovered

### 2. Model Architecture Evolution

Track model architecture changes over time:

```hcl
resource "ml_model" "production_model" {
  name         = "recommendation-engine"
  framework    = "pytorch"
  architecture = "transformer"
  version      = "2.0.0"

  hyperparameters = {
    hidden_size     = "512"  # v1.0 used 256
    num_layers      = "12"   # v1.0 used 6
    attention_heads = "8"
    dropout         = "0.1"
  }
}

# Track in git:
# v1.0: 6 layers, 256 hidden, 85% accuracy
# v2.0: 12 layers, 512 hidden, 92% accuracy
# Full history of architecture evolution
```

**Why This Matters**:
- A/B test different architectures declaratively
- Rollback to previous architecture if needed
- Document why architecture changed (git commit messages)
- Reproduce old model versions exactly

### 3. Experiment Tracking and Comparison

Compare multiple experiments declaratively:

```hcl
# Baseline experiment
resource "ml_training_job" "baseline" {
  name         = "baseline-v1"
  model_id     = ml_model.bert.id
  dataset_id   = ml_dataset.reviews.id
  learning_rate = 0.001
  epochs       = 10
}

# Experiment: Higher learning rate
resource "ml_training_job" "high_lr" {
  name         = "high-lr-v1"
  model_id     = ml_model.bert.id
  dataset_id   = ml_dataset.reviews.id
  learning_rate = 0.01  # 10x higher
  epochs       = 10
}

# Query both experiments
data "ml_experiment_metrics" "baseline_metrics" {
  experiment_id = ml_training_job.baseline.experiment_id
}

data "ml_experiment_metrics" "high_lr_metrics" {
  experiment_id = ml_training_job.high_lr.experiment_id
}

# Compare results
output "experiment_comparison" {
  value = {
    baseline_accuracy = data.ml_experiment_metrics.baseline_metrics.best_metric_value
    high_lr_accuracy  = data.ml_experiment_metrics.high_lr_metrics.best_metric_value
    winner = (
      data.ml_experiment_metrics.high_lr_metrics.best_metric_value >
      data.ml_experiment_metrics.baseline_metrics.best_metric_value
      ? "high_lr" : "baseline"
    )
  }
}
```

**Expected Output**:
```
experiment_comparison = {
  baseline_accuracy = 0.89
  high_lr_accuracy  = 0.92
  winner            = "high_lr"
}
```

### 4. Hyperparameter Tuning Grid

Declarative hyperparameter search:

```hcl
locals {
  learning_rates = [0.0001, 0.001, 0.01]
  batch_sizes    = [16, 32, 64]

  # Generate all combinations
  hp_configs = [
    for lr in local.learning_rates : [
      for bs in local.batch_sizes : {
        learning_rate = lr
        batch_size    = bs
      }
    ]
  ]
  hp_configs_flat = flatten(local.hp_configs)
}

# Run all combinations
resource "ml_training_job" "hp_search" {
  count = length(local.hp_configs_flat)

  name          = "hp-search-${count.index}"
  model_id      = ml_model.classifier.id
  dataset_id    = ml_dataset.train.id
  learning_rate = local.hp_configs_flat[count.index].learning_rate
  batch_size    = local.hp_configs_flat[count.index].batch_size
  epochs        = 20

  tags = {
    Experiment    = "hp-grid-search"
    LearningRate  = tostring(local.hp_configs_flat[count.index].learning_rate)
    BatchSize     = tostring(local.hp_configs_flat[count.index].batch_size)
  }
}

# Find best configuration
output "best_hyperparameters" {
  value = {
    best_job_id = data.ml_experiment_metrics.hp_results.best_run_id
    best_config = local.hp_configs_flat[
      index(
        ml_training_job.hp_search[*].job_id,
        data.ml_experiment_metrics.hp_results.best_run_id
      )
    ]
  }
}
```

**Why This Matters**:
- Systematic hyperparameter exploration
- Reproducible tuning process
- Compare all configurations side-by-side
- Version control tuning strategy

### 5. Model Promotion Pipeline

Automate model staging and production promotion:

```hcl
# Train candidate model
resource "ml_training_job" "candidate" {
  name       = "production-candidate-v3"
  model_id   = ml_model.production.id
  dataset_id = ml_dataset.latest.id
  # ... training config
}

# Query current production model
data "ml_model_registry" "current_production" {
  filter_stage = "production"
}

# Conditional promotion logic
locals {
  candidate_accuracy = ml_training_job.candidate.val_accuracy
  production_accuracy = data.ml_model_registry.current_production.models[0].accuracy

  # Promote if candidate is 2% better
  should_promote = local.candidate_accuracy > (local.production_accuracy + 0.02)
}

output "promotion_decision" {
  value = {
    should_promote       = local.should_promote
    candidate_accuracy   = local.candidate_accuracy
    production_accuracy  = local.production_accuracy
    improvement_percent  = (local.candidate_accuracy - local.production_accuracy) * 100
    decision             = local.should_promote ? "PROMOTE" : "REJECT"
  }
}
```

**Why This Matters**:
- Automated quality gates
- Codified promotion criteria
- Audit trail of deployment decisions
- Rollback capability

---

## Project Structure

```
ml-provider/
├── provider.py          # Provider implementation
│   ├── MLDataset        # Versioned dataset resource
│   ├── MLModel          # Model architecture resource
│   ├── TrainingJob      # Training orchestration resource
│   ├── ExperimentMetrics # Query experiment results
│   ├── ModelRegistry    # Query model registry
│   └── 4 Functions      # ML utility functions
├── pyproject.toml       # Python project configuration
├── pyvider.toml         # Pyvider runtime configuration
├── example.tf           # Comprehensive examples
└── README.md            # This file
```

---

## API Reference

### Provider Configuration

```hcl
provider "ml" {
  experiment_tracking_uri = "http://mlflow:5000"  # MLflow server
  model_registry_uri      = "s3://models/"        # Model storage
  default_framework       = "pytorch"              # Default framework
  enable_gpu              = true                   # Enable GPU training
  random_seed             = 42                     # Reproducibility
}
```

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `experiment_tracking_uri` | string | `file:///tmp/mlruns` | Experiment tracking backend |
| `model_registry_uri` | string | `file:///tmp/models` | Model registry storage |
| `default_framework` | string | `"pytorch"` | Default ML framework |
| `enable_gpu` | bool | `false` | Enable GPU acceleration |
| `random_seed` | int | `42` | Random seed for reproducibility |

### Resources

#### ml_dataset

Versioned dataset with validation and preprocessing.

```hcl
resource "ml_dataset" "example" {
  name       = "dataset-name"
  source_uri = "s3://bucket/path"
  version    = "1.0.0"
  format     = "parquet"

  schema = {
    feature1 = "float"
    feature2 = "int"
    label    = "string"
  }

  split_ratios = {
    train = 0.7
    val   = 0.15
    test  = 0.15
  }

  preprocessing = [
    "normalize",
    "fill_missing",
  ]

  validation_rules = {
    no_nulls = "required"
  }

  tags = {
    Team = "ml-research"
  }
}
```

**Attributes**:

| Attribute | Type | Required | Computed | Description |
|-----------|------|----------|----------|-------------|
| `name` | string | Yes | No | Dataset name |
| `source_uri` | string | Yes | No | Data source URI |
| `version` | string | No | No | Dataset version (default: "1.0.0") |
| `format` | string | No | No | Data format (csv, parquet, json) |
| `schema` | map(string) | No | No | Column schema |
| `split_ratios` | map(number) | No | No | Train/val/test splits |
| `preprocessing` | list(string) | No | No | Preprocessing steps |
| `validation_rules` | map(string) | No | No | Validation rules |
| `tags` | map(string) | No | No | Tags |
| `dataset_id` | string | No | Yes | Unique dataset ID |
| `row_count` | number | No | Yes | Total rows |
| `column_count` | number | No | Yes | Number of columns |
| `size_bytes` | number | No | Yes | Dataset size |
| `checksum` | string | No | Yes | Data checksum |
| `train_rows` | number | No | Yes | Training set size |
| `val_rows` | number | No | Yes | Validation set size |
| `test_rows` | number | No | Yes | Test set size |
| `created_at` | string | No | Yes | Creation timestamp |
| `status` | string | No | Yes | Dataset status |

#### ml_model

Model architecture definition with versioning.

```hcl
resource "ml_model" "example" {
  name         = "model-name"
  framework    = "pytorch"
  architecture = "resnet50"
  version      = "1.0.0"

  hyperparameters = {
    num_classes = "1000"
    dropout     = "0.5"
  }

  input_schema = {
    images = "tensor[batch, 3, 224, 224]"
  }

  output_schema = {
    logits = "tensor[batch, 1000]"
  }

  pretrained_weights = "s3://models/resnet50.pth"

  tags = {
    Architecture = "cnn"
  }
}
```

**Attributes**:

| Attribute | Type | Required | Computed | Description |
|-----------|------|----------|----------|-------------|
| `name` | string | Yes | No | Model name |
| `framework` | string | Yes | No | ML framework |
| `architecture` | string | Yes | No | Model architecture |
| `version` | string | No | No | Model version |
| `hyperparameters` | map(string) | No | No | Hyperparameters (JSON strings) |
| `input_schema` | map(string) | No | No | Input tensor schema |
| `output_schema` | map(string) | No | No | Output schema |
| `pretrained_weights` | string | No | No | Pretrained weights URI |
| `tags` | map(string) | No | No | Tags |
| `model_id` | string | No | Yes | Unique model ID |
| `parameter_count` | number | No | Yes | Number of parameters |
| `size_bytes` | number | No | Yes | Model size |
| `model_uri` | string | No | Yes | Model storage URI |
| `checksum` | string | No | Yes | Weights checksum |
| `created_at` | string | No | Yes | Creation timestamp |
| `status` | string | No | Yes | Model status |

#### ml_training_job

Training job orchestration with experiment tracking.

```hcl
resource "ml_training_job" "example" {
  name       = "training-job-name"
  model_id   = ml_model.example.model_id
  dataset_id = ml_dataset.example.dataset_id

  epochs         = 50
  batch_size     = 32
  learning_rate  = 0.001
  optimizer      = "adam"
  loss_function  = "cross_entropy"

  metrics = ["accuracy", "f1_score"]

  early_stopping       = true
  patience             = 5
  checkpoint_frequency = 1

  distributed = true
  num_gpus    = 4

  tags = {
    Experiment = "baseline"
  }
}
```

**Attributes**:

| Attribute | Type | Required | Computed | Description |
|-----------|------|----------|----------|-------------|
| `name` | string | Yes | No | Job name |
| `model_id` | string | Yes | No | Model to train |
| `dataset_id` | string | Yes | No | Training dataset |
| `epochs` | number | No | No | Number of epochs (default: 10) |
| `batch_size` | number | No | No | Batch size (default: 32) |
| `learning_rate` | number | No | No | Learning rate (default: 0.001) |
| `optimizer` | string | No | No | Optimizer (default: "adam") |
| `loss_function` | string | No | No | Loss function |
| `metrics` | list(string) | No | No | Metrics to track |
| `early_stopping` | bool | No | No | Enable early stopping |
| `patience` | number | No | No | Early stopping patience |
| `checkpoint_frequency` | number | No | No | Checkpoint every N epochs |
| `distributed` | bool | No | No | Use distributed training |
| `num_gpus` | number | No | No | Number of GPUs |
| `tags` | map(string) | No | No | Tags |
| `job_id` | string | No | Yes | Unique job ID |
| `experiment_id` | string | No | Yes | Experiment ID |
| `run_id` | string | No | Yes | Run ID |
| `status` | string | No | Yes | Job status |
| `current_epoch` | number | No | Yes | Current epoch |
| `best_epoch` | number | No | Yes | Best epoch |
| `train_loss` | number | No | Yes | Training loss |
| `val_loss` | number | No | Yes | Validation loss |
| `best_val_loss` | number | No | Yes | Best validation loss |
| `train_accuracy` | number | No | Yes | Training accuracy |
| `val_accuracy` | number | No | Yes | Validation accuracy |
| `best_val_accuracy` | number | No | Yes | Best validation accuracy |
| `training_time_seconds` | number | No | Yes | Training time |
| `checkpoint_uri` | string | No | Yes | Best checkpoint URI |
| `logs_uri` | string | No | Yes | Logs URI |
| `started_at` | string | No | Yes | Start time |
| `completed_at` | string | No | Yes | Completion time |

### Data Sources

#### ml_experiment_metrics

Query metrics from ML experiments.

```hcl
data "ml_experiment_metrics" "results" {
  experiment_id = "exp-123"
  metric_names  = ["accuracy", "loss"]
  filter_tags   = {
    Experiment = "baseline"
  }
}
```

**Attributes**:

| Attribute | Type | Description |
|-----------|------|-------------|
| `experiment_id` | string | Experiment ID (optional) |
| `metric_names` | list(string) | Metrics to retrieve (optional) |
| `filter_tags` | map(string) | Filter by tags (optional) |
| `id` | string | Query ID (computed) |
| `runs` | list(object) | Experiment runs (computed) |
| `best_run_id` | string | Best run ID (computed) |
| `best_metric_value` | number | Best metric value (computed) |

#### ml_model_registry

Query model registry.

```hcl
data "ml_model_registry" "production" {
  filter_framework = "pytorch"
  filter_stage     = "production"
  min_accuracy     = 0.90
}
```

**Attributes**:

| Attribute | Type | Description |
|-----------|------|-------------|
| `filter_framework` | string | Filter by framework (optional) |
| `filter_stage` | string | Filter by stage (optional) |
| `min_accuracy` | number | Minimum accuracy (optional) |
| `id` | string | Query ID (computed) |
| `models` | list(object) | Registered models (computed) |
| `count` | number | Number of models (computed) |

### Functions

#### provider::ml::calculate_metrics

Calculate evaluation metrics.

```hcl
locals {
  accuracy = provider::ml::calculate_metrics(
    predictions, # list(number)
    labels,      # list(number)
    "accuracy"   # metric type
  )
}
```

**Metrics**: `accuracy`, `mse`, `mae`, `rmse`

#### provider::ml::split_dataset

Calculate dataset split sizes.

```hcl
locals {
  splits = provider::ml::split_dataset(
    10000, # total_size
    0.7,   # train_ratio
    0.15,  # val_ratio
    0.15   # test_ratio
  )
  # Returns: {train: 7000, val: 1500, test: 1500}
}
```

#### provider::ml::estimate_training_time

Estimate training time in seconds.

```hcl
locals {
  seconds = provider::ml::estimate_training_time(
    10000,     # dataset_rows
    50000000,  # model_parameters
    32,        # batch_size
    50,        # epochs
    true       # gpu_enabled
  )
}
```

#### provider::ml::generate_model_name

Generate standardized model names.

```hcl
locals {
  name = provider::ml::generate_model_name(
    "classification", # task
    "pytorch",        # framework
    "ResNet-50",      # architecture
    "v1.0"            # version
  )
  # Returns: "classification-pytorch-resnet50-v1.0"
}
```

---

## Use Cases

### 1. MLOps Pipeline Automation

Automate the entire ML pipeline from data to deployment:

- **Data versioning**: Track dataset changes
- **Experiment management**: Reproducible training
- **Model registry**: Automated promotion
- **Infrastructure as code**: Version controlled ML ops

### 2. Research Experiment Tracking

Academic and research teams:

- **Experiment reproducibility**: Git commits = reproducible experiments
- **Collaboration**: Pull request workflow for experiments
- **Comparison**: Side-by-side experiment comparison
- **Documentation**: Git history documents research process

### 3. Production ML Deployment

Production ML systems:

- **Canary deployments**: Gradual model rollouts
- **A/B testing**: Compare model versions in production
- **Rollback**: Instant rollback to previous model version
- **Audit compliance**: Full deployment history

### 4. Multi-Team ML Platform

Platform teams supporting multiple ML teams:

- **Resource management**: Manage datasets, models across teams
- **Access control**: Team-based permissions via Terraform
- **Cost tracking**: Track training costs per team
- **Standardization**: Enforce ML best practices via Terraform modules

---

## Comparison with Traditional Approaches

### vs. MLflow

| Feature | MLflow | ML Provider (Terraform) |
|---------|--------|-------------------------|
| API | Imperative (Python API) | Declarative (HCL) |
| Version Control | Manual | Native (git) |
| Reproducibility | Tracking only | Full infrastructure |
| Collaboration | Manual sharing | Pull requests |
| Deployment | Separate tool | Integrated |
| Rollback | Manual | `terraform apply` old config |

### vs. Kubeflow

| Feature | Kubeflow | ML Provider |
|---------|----------|-------------|
| Complexity | High (Kubernetes) | Low (Terraform) |
| Learning Curve | Steep | Gentle (if know Terraform) |
| Infrastructure | K8s required | Any Terraform target |
| Workflow | Custom pipelines | Terraform DAG |
| Integration | K8s ecosystem | Terraform ecosystem |

### vs. SageMaker

| Feature | SageMaker | ML Provider |
|---------|-----------|-------------|
| Cloud | AWS only | Cloud-agnostic |
| API | Boto3 (imperative) | Terraform (declarative) |
| Cost | AWS pricing | Any infrastructure |
| Lock-in | High | None |
| Customization | Limited | Full control |

---

## Advanced Patterns

### 1. Multi-Environment ML

Manage dev/staging/prod ML infrastructure:

```hcl
# modules/ml-environment/main.tf
variable "environment" {
  type = string
}

resource "ml_dataset" "data" {
  name       = "dataset-${var.environment}"
  source_uri = "s3://data/${var.environment}/"
  version    = var.environment == "prod" ? "1.0.0" : "dev"
}

resource "ml_model" "model" {
  name      = "model-${var.environment}"
  framework = "pytorch"
  # Production uses larger model
  architecture = var.environment == "prod" ? "large" : "small"
}

# Use module
module "dev_ml" {
  source      = "./modules/ml-environment"
  environment = "dev"
}

module "prod_ml" {
  source      = "./modules/ml-environment"
  environment = "prod"
}
```

### 2. Conditional Model Training

Train only if data or model changed:

```hcl
locals {
  # Hash of model config
  model_hash = md5(jsonencode(ml_model.classifier))

  # Hash of dataset config
  dataset_hash = ml_dataset.train.checksum

  # Combined hash for training decision
  training_hash = md5("${local.model_hash}-${local.dataset_hash}")
}

resource "ml_training_job" "conditional" {
  # Only train if hash changed
  count = local.training_hash != var.last_training_hash ? 1 : 0

  name       = "conditional-training-${local.training_hash}"
  model_id   = ml_model.classifier.id
  dataset_id = ml_dataset.train.id
  # ...
}
```

### 3. Automated Model Registry

Automatically register models that meet quality thresholds:

```hcl
# Train model
resource "ml_training_job" "candidate" {
  # ... training config
}

# Register if accuracy > 90%
resource "ml_model_version" "production" {
  count = ml_training_job.candidate.val_accuracy > 0.90 ? 1 : 0

  model_id   = ml_model.classifier.id
  version    = "prod-${formatdate("YYYY-MM-DD", timestamp())}"
  stage      = "production"
  checkpoint = ml_training_job.candidate.checkpoint_uri
}
```

---

## Development

### Running Tests

```bash
pytest tests/
```

### Type Checking

```bash
mypy provider.py
```

### Linting

```bash
ruff check provider.py
ruff format provider.py
```

---

## Future Enhancements

Potential production features:

1. **Real MLflow Integration**: Connect to actual MLflow servers
2. **Distributed Training**: Kubernetes/Ray integration
3. **AutoML**: Automated hyperparameter tuning
4. **Model Monitoring**: Production model performance tracking
5. **Feature Store**: Feature engineering as infrastructure
6. **Pipeline Orchestration**: Multi-stage ML pipelines
7. **Cost Optimization**: Automatic spot instance usage

---

## Resources

### Machine Learning

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [Kubeflow](https://www.kubeflow.org/)
- [DVC (Data Version Control)](https://dvc.org/)

### ML Best Practices

- [Google - Rules of ML](https://developers.google.com/machine-learning/guides/rules-of-ml)
- [Hidden Technical Debt in ML Systems](https://papers.nips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html)
- [ML Test Score](https://research.google/pubs/pub46555/)

### Pyvider

- [Pyvider Documentation](https://foundry.provide.io/pyvider/)
- [Terraform Provider Protocol](https://developer.hashicorp.com/terraform/plugin/terraform-plugin-protocol)

---

## Contributing

Ideas for additional ML features:

- **Feature Store**: Centralized feature management
- **Data Quality**: Automated data validation
- **Model Explainability**: SHAP/LIME integration
- **Automated Retraining**: Trigger on data drift
- **Multi-Modal Models**: Vision + text models
- **Federated Learning**: Distributed training patterns

---

## License

Apache 2.0 - See [LICENSE](../../LICENSE) for details.

---

**Made with ❤️ using [Pyvider](https://github.com/provide-io/pyvider)**

*Demonstrating that ML workflows are infrastructure and should be managed declaratively.*
