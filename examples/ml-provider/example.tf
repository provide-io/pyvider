# Machine Learning Provider - Comprehensive Example
#
# This example demonstrates ML infrastructure as code:
# - Dataset management with versioning
# - Model definition and versioning
# - Training job orchestration
# - Experiment tracking and metrics
# - Model registry queries
# - ML utility functions

terraform {
  required_providers {
    ml = {
      source  = "local/provide/ml"
      version = "1.0.0"
    }
  }
}

# ============================================================================
# Provider Configuration
# ============================================================================

provider "ml" {
  experiment_tracking_uri = "http://mlflow.example.com:5000"
  model_registry_uri      = "s3://my-models-bucket/registry"
  default_framework       = "pytorch"
  enable_gpu              = true
  random_seed             = 42
}

# ============================================================================
# Datasets - Versioned Training Data
# ============================================================================

# Image classification dataset
resource "ml_dataset" "imagenet_subset" {
  name       = "imagenet-subset-v1"
  source_uri = "s3://datasets/imagenet/subset/"
  version    = "1.0.0"
  format     = "parquet"

  schema = {
    image_path = "string"
    label      = "int"
    split      = "string"
  }

  split_ratios = {
    train = 0.7
    val   = 0.15
    test  = 0.15
  }

  preprocessing = [
    "resize_224x224",
    "normalize_imagenet",
    "random_horizontal_flip",
    "random_rotation_15"
  ]

  validation_rules = {
    image_exists    = "check_file_exists"
    label_in_range  = "0-999"
    split_not_empty = "required"
  }

  tags = {
    Team        = "ml-research"
    Project     = "image-classification"
    DatasetType = "vision"
  }
}

# Text classification dataset
resource "ml_dataset" "sentiment_analysis" {
  name       = "sentiment-reviews"
  source_uri = "s3://datasets/reviews/2024/"
  version    = "2.0.0"
  format     = "csv"

  schema = {
    text      = "string"
    sentiment = "int"
    rating    = "float"
  }

  split_ratios = {
    train = 0.8
    val   = 0.1
    test  = 0.1
  }

  preprocessing = [
    "lowercase",
    "remove_punctuation",
    "tokenize",
    "remove_stopwords",
  ]

  validation_rules = {
    text_not_empty  = "required"
    sentiment_range = "0-2"
  }

  tags = {
    Team    = "nlp-team"
    Project = "sentiment-analysis"
    Domain  = "reviews"
  }
}

# Time series dataset
resource "ml_dataset" "stock_prices" {
  name       = "sp500-daily"
  source_uri = "s3://datasets/finance/sp500/"
  version    = "1.5.0"
  format     = "parquet"

  schema = {
    date   = "datetime"
    ticker = "string"
    open   = "float"
    high   = "float"
    low    = "float"
    close  = "float"
    volume = "int"
  }

  split_ratios = {
    train = 0.7
    val   = 0.15
    test  = 0.15
  }

  preprocessing = [
    "fill_missing_values",
    "normalize_prices",
    "create_technical_indicators",
  ]

  tags = {
    Team     = "quant-team"
    Project  = "stock-prediction"
    Interval = "daily"
  }
}

# ============================================================================
# Models - ML Model Definitions
# ============================================================================

# ResNet50 for image classification
resource "ml_model" "resnet50_classifier" {
  name         = "resnet50-imagenet"
  framework    = "pytorch"
  architecture = "resnet50"
  version      = "1.0.0"

  hyperparameters = {
    num_classes      = "1000"
    dropout_rate     = "0.5"
    use_pretrained   = "true"
    freeze_backbone  = "false"
    activation       = "relu"
    normalization    = "batch_norm"
  }

  input_schema = {
    images = "tensor[batch, 3, 224, 224]"
  }

  output_schema = {
    logits      = "tensor[batch, 1000]"
    predictions = "tensor[batch]"
    probabilities = "tensor[batch, 1000]"
  }

  pretrained_weights = "s3://models/resnet50/imagenet_weights.pth"

  tags = {
    Architecture = "cnn"
    Task         = "classification"
    Domain       = "vision"
  }
}

# BERT for text classification
resource "ml_model" "bert_sentiment" {
  name         = "bert-base-sentiment"
  framework    = "pytorch"
  architecture = "bert-base-uncased"
  version      = "1.0.0"

  hyperparameters = {
    num_labels       = "3"
    hidden_size      = "768"
    num_layers       = "12"
    num_heads        = "12"
    dropout          = "0.1"
    max_seq_length   = "512"
  }

  input_schema = {
    input_ids      = "tensor[batch, seq_len]"
    attention_mask = "tensor[batch, seq_len]"
    token_type_ids = "tensor[batch, seq_len]"
  }

  output_schema = {
    logits = "tensor[batch, 3]"
    predictions = "tensor[batch]"
  }

  pretrained_weights = "s3://models/bert/bert-base-uncased.pth"

  tags = {
    Architecture = "transformer"
    Task         = "classification"
    Domain       = "nlp"
  }
}

# LSTM for time series forecasting
resource "ml_model" "lstm_forecaster" {
  name         = "lstm-stock-predictor"
  framework    = "tensorflow"
  architecture = "lstm-seq2seq"
  version      = "1.0.0"

  hyperparameters = {
    hidden_units    = "128"
    num_layers      = "2"
    dropout         = "0.2"
    bidirectional   = "true"
    lookback_window = "30"
    forecast_horizon = "5"
  }

  input_schema = {
    historical_prices = "tensor[batch, 30, 7]"  # 30 days, 7 features
  }

  output_schema = {
    predicted_prices = "tensor[batch, 5]"  # 5 days forecast
  }

  tags = {
    Architecture = "rnn"
    Task         = "forecasting"
    Domain       = "finance"
  }
}

# ============================================================================
# Training Jobs - ML Training Orchestration
# ============================================================================

# Train ResNet50 on ImageNet subset
resource "ml_training_job" "train_resnet" {
  name       = "resnet50-imagenet-v1"
  model_id   = ml_model.resnet50_classifier.model_id
  dataset_id = ml_dataset.imagenet_subset.dataset_id

  epochs      = 50
  batch_size  = 64
  learning_rate = 0.001

  optimizer     = "adam"
  loss_function = "cross_entropy"

  metrics = [
    "accuracy",
    "top5_accuracy",
    "f1_score",
    "precision",
    "recall",
  ]

  early_stopping      = true
  patience            = 10
  checkpoint_frequency = 1

  distributed = true
  num_gpus    = 4

  tags = {
    Experiment = "baseline-resnet"
    Priority   = "high"
  }
}

# Train BERT for sentiment analysis
resource "ml_training_job" "train_bert" {
  name       = "bert-sentiment-v1"
  model_id   = ml_model.bert_sentiment.model_id
  dataset_id = ml_dataset.sentiment_analysis.dataset_id

  epochs      = 10
  batch_size  = 32
  learning_rate = 2e-5

  optimizer     = "adamw"
  loss_function = "cross_entropy"

  metrics = [
    "accuracy",
    "f1_macro",
    "confusion_matrix",
  ]

  early_stopping      = true
  patience            = 3
  checkpoint_frequency = 1

  distributed = false
  num_gpus    = 1

  tags = {
    Experiment = "sentiment-bert-baseline"
    Priority   = "medium"
  }
}

# Train LSTM forecaster
resource "ml_training_job" "train_lstm" {
  name       = "lstm-stock-v1"
  model_id   = ml_model.lstm_forecaster.model_id
  dataset_id = ml_dataset.stock_prices.dataset_id

  epochs      = 100
  batch_size  = 128
  learning_rate = 0.001

  optimizer     = "rmsprop"
  loss_function = "mse"

  metrics = [
    "mse",
    "mae",
    "rmse",
    "mape",
  ]

  early_stopping      = true
  patience            = 15
  checkpoint_frequency = 5

  distributed = false
  num_gpus    = 1

  tags = {
    Experiment = "lstm-baseline"
    Timeframe  = "daily"
  }
}

# Hyperparameter tuning job (multiple configurations)
resource "ml_training_job" "resnet_hp_tuning" {
  count = 3

  name       = "resnet50-hp-tune-${count.index + 1}"
  model_id   = ml_model.resnet50_classifier.model_id
  dataset_id = ml_dataset.imagenet_subset.dataset_id

  epochs     = 30
  batch_size = 64

  # Different learning rates for tuning
  learning_rate = [0.0001, 0.001, 0.01][count.index]

  optimizer     = "adam"
  loss_function = "cross_entropy"

  metrics = ["accuracy", "loss"]

  early_stopping      = true
  patience            = 5
  checkpoint_frequency = 5

  distributed = false
  num_gpus    = 1

  tags = {
    Experiment   = "hp-tuning"
    LearningRate = tostring([0.0001, 0.001, 0.01][count.index])
    Run          = tostring(count.index + 1)
  }
}

# ============================================================================
# Data Sources - Query ML Experiments and Registry
# ============================================================================

# Query ResNet experiment metrics
data "ml_experiment_metrics" "resnet_results" {
  experiment_id = ml_training_job.train_resnet.experiment_id

  metric_names = [
    "accuracy",
    "val_accuracy",
    "loss",
    "val_loss",
  ]

  filter_tags = {
    Experiment = "baseline-resnet"
  }

  depends_on = [ml_training_job.train_resnet]
}

# Query BERT experiment metrics
data "ml_experiment_metrics" "bert_results" {
  experiment_id = ml_training_job.train_bert.experiment_id

  metric_names = [
    "accuracy",
    "f1_macro",
  ]

  depends_on = [ml_training_job.train_bert]
}

# Query hyperparameter tuning results
data "ml_experiment_metrics" "hp_tuning_results" {
  experiment_id = ml_training_job.resnet_hp_tuning[0].experiment_id

  metric_names = ["val_accuracy"]

  filter_tags = {
    Experiment = "hp-tuning"
  }

  depends_on = [ml_training_job.resnet_hp_tuning]
}

# Query production-ready models from registry
data "ml_model_registry" "production_models" {
  filter_framework = "pytorch"
  filter_stage     = "production"
  min_accuracy     = 0.90
}

# Query staging models for review
data "ml_model_registry" "staging_models" {
  filter_stage = "staging"
  min_accuracy = 0.85
}

# Query all TensorFlow models
data "ml_model_registry" "tensorflow_models" {
  filter_framework = "tensorflow"
}

# ============================================================================
# Local Values - Using Provider Functions
# ============================================================================

locals {
  # Calculate dataset splits
  imagenet_splits = provider::ml::split_dataset(
    ml_dataset.imagenet_subset.row_count,
    0.7,
    0.15,
    0.15
  )

  sentiment_splits = provider::ml::split_dataset(
    ml_dataset.sentiment_analysis.row_count,
    0.8,
    0.1,
    0.1
  )

  # Estimate training times
  resnet_training_time = provider::ml::estimate_training_time(
    local.imagenet_splits["train"],
    ml_model.resnet50_classifier.parameter_count,
    64,  # batch_size
    50,  # epochs
    true # gpu_enabled
  )

  bert_training_time = provider::ml::estimate_training_time(
    local.sentiment_splits["train"],
    ml_model.bert_sentiment.parameter_count,
    32,
    10,
    true
  )

  lstm_training_time = provider::ml::estimate_training_time(
    ml_dataset.stock_prices.train_rows,
    ml_model.lstm_forecaster.parameter_count,
    128,
    100,
    true
  )

  # Generate standardized model names
  resnet_model_name = provider::ml::generate_model_name(
    "image classification",
    "pytorch",
    "ResNet-50",
    "v1.0"
  )

  bert_model_name = provider::ml::generate_model_name(
    "text classification",
    "pytorch",
    "BERT Base",
    "v1.0"
  )

  lstm_model_name = provider::ml::generate_model_name(
    "time series forecasting",
    "tensorflow",
    "LSTM Seq2Seq",
    "v1.0"
  )

  # Calculate metrics for validation
  # Example predictions and labels
  sample_predictions = [0.9, 0.8, 0.7, 0.95, 0.6]
  sample_labels      = [1.0, 1.0, 0.0, 1.0, 1.0]

  accuracy_score = provider::ml::calculate_metrics(
    local.sample_predictions,
    local.sample_labels,
    "accuracy"
  )

  mse_score = provider::ml::calculate_metrics(
    local.sample_predictions,
    local.sample_labels,
    "mse"
  )

  mae_score = provider::ml::calculate_metrics(
    local.sample_predictions,
    local.sample_labels,
    "mae"
  )

  # Training time summary
  total_training_time_hours = (
    local.resnet_training_time +
    local.bert_training_time +
    local.lstm_training_time
  ) / 3600

  # Cost estimation (assuming $1/GPU-hour)
  estimated_training_cost = local.total_training_time_hours * (
    ml_training_job.train_resnet.num_gpus +
    ml_training_job.train_bert.num_gpus +
    ml_training_job.train_lstm.num_gpus
  )
}

# ============================================================================
# Outputs - ML Infrastructure Insights
# ============================================================================

# Dataset Information
output "imagenet_dataset_id" {
  description = "ImageNet subset dataset ID"
  value       = ml_dataset.imagenet_subset.dataset_id
}

output "imagenet_stats" {
  description = "ImageNet dataset statistics"
  value = {
    total_rows    = ml_dataset.imagenet_subset.row_count
    train_rows    = ml_dataset.imagenet_subset.train_rows
    val_rows      = ml_dataset.imagenet_subset.val_rows
    test_rows     = ml_dataset.imagenet_subset.test_rows
    columns       = ml_dataset.imagenet_subset.column_count
    size_mb       = ml_dataset.imagenet_subset.size_bytes / 1024 / 1024
    checksum      = ml_dataset.imagenet_subset.checksum
  }
}

output "all_datasets" {
  description = "Summary of all datasets"
  value = {
    imagenet = {
      id      = ml_dataset.imagenet_subset.dataset_id
      rows    = ml_dataset.imagenet_subset.row_count
      version = ml_dataset.imagenet_subset.version
    }
    sentiment = {
      id      = ml_dataset.sentiment_analysis.dataset_id
      rows    = ml_dataset.sentiment_analysis.row_count
      version = ml_dataset.sentiment_analysis.version
    }
    stock = {
      id      = ml_dataset.stock_prices.dataset_id
      rows    = ml_dataset.stock_prices.row_count
      version = ml_dataset.stock_prices.version
    }
  }
}

# Model Information
output "resnet_model_info" {
  description = "ResNet50 model information"
  value = {
    model_id    = ml_model.resnet50_classifier.model_id
    parameters  = ml_model.resnet50_classifier.parameter_count
    size_mb     = ml_model.resnet50_classifier.size_bytes / 1024 / 1024
    uri         = ml_model.resnet50_classifier.model_uri
    status      = ml_model.resnet50_classifier.status
  }
}

output "all_models" {
  description = "Summary of all models"
  value = {
    resnet = {
      id         = ml_model.resnet50_classifier.model_id
      framework  = ml_model.resnet50_classifier.framework
      parameters = ml_model.resnet50_classifier.parameter_count
    }
    bert = {
      id         = ml_model.bert_sentiment.model_id
      framework  = ml_model.bert_sentiment.framework
      parameters = ml_model.bert_sentiment.parameter_count
    }
    lstm = {
      id         = ml_model.lstm_forecaster.model_id
      framework  = ml_model.lstm_forecaster.framework
      parameters = ml_model.lstm_forecaster.parameter_count
    }
  }
}

# Training Job Results
output "resnet_training_results" {
  description = "ResNet training job results"
  value = {
    job_id            = ml_training_job.train_resnet.job_id
    status            = ml_training_job.train_resnet.status
    final_epoch       = ml_training_job.train_resnet.current_epoch
    best_epoch        = ml_training_job.train_resnet.best_epoch
    train_accuracy    = ml_training_job.train_resnet.train_accuracy
    val_accuracy      = ml_training_job.train_resnet.val_accuracy
    best_val_accuracy = ml_training_job.train_resnet.best_val_accuracy
    training_time_min = ml_training_job.train_resnet.training_time_seconds / 60
    checkpoint_uri    = ml_training_job.train_resnet.checkpoint_uri
  }
}

output "bert_training_results" {
  description = "BERT training job results"
  value = {
    job_id            = ml_training_job.train_bert.job_id
    status            = ml_training_job.train_bert.status
    val_accuracy      = ml_training_job.train_bert.val_accuracy
    best_val_accuracy = ml_training_job.train_bert.best_val_accuracy
    training_time_min = ml_training_job.train_bert.training_time_seconds / 60
  }
}

output "lstm_training_results" {
  description = "LSTM training job results"
  value = {
    job_id         = ml_training_job.train_lstm.job_id
    status         = ml_training_job.train_lstm.status
    final_loss     = ml_training_job.train_lstm.val_loss
    best_loss      = ml_training_job.train_lstm.best_val_loss
    training_time_hr = ml_training_job.train_lstm.training_time_seconds / 3600
  }
}

# Hyperparameter Tuning Results
output "hp_tuning_summary" {
  description = "Hyperparameter tuning results"
  value = {
    runs = [
      for job in ml_training_job.resnet_hp_tuning : {
        job_id       = job.job_id
        learning_rate = job.learning_rate
        val_accuracy = job.val_accuracy
        best_epoch   = job.best_epoch
      }
    ]
    best_run_id = data.ml_experiment_metrics.hp_tuning_results.best_run_id
    best_accuracy = data.ml_experiment_metrics.hp_tuning_results.best_metric_value
  }
}

# Experiment Metrics
output "resnet_experiment_metrics" {
  description = "ResNet experiment detailed metrics"
  value = {
    experiment_id = data.ml_experiment_metrics.resnet_results.id
    runs          = data.ml_experiment_metrics.resnet_results.runs
    best_run      = data.ml_experiment_metrics.resnet_results.best_run_id
  }
}

output "bert_experiment_metrics" {
  description = "BERT experiment metrics"
  value = {
    runs     = data.ml_experiment_metrics.bert_results.runs
    best_run = data.ml_experiment_metrics.bert_results.best_run_id
  }
}

# Model Registry Queries
output "production_models" {
  description = "Models in production"
  value = {
    count  = data.ml_model_registry.production_models.count
    models = data.ml_model_registry.production_models.models
  }
}

output "staging_models" {
  description = "Models in staging for review"
  value = {
    count  = data.ml_model_registry.staging_models.count
    models = data.ml_model_registry.staging_models.models
  }
}

# Calculated Metrics
output "dataset_split_details" {
  description = "Calculated dataset splits"
  value = {
    imagenet = local.imagenet_splits
    sentiment = local.sentiment_splits
  }
}

output "training_time_estimates" {
  description = "Estimated training times (seconds)"
  value = {
    resnet_seconds = local.resnet_training_time
    bert_seconds   = local.bert_training_time
    lstm_seconds   = local.lstm_training_time
    total_hours    = local.total_training_time_hours
  }
}

output "training_cost_estimate" {
  description = "Estimated training cost in USD"
  value       = local.estimated_training_cost
}

output "generated_model_names" {
  description = "Standardized model names"
  value = {
    resnet = local.resnet_model_name
    bert   = local.bert_model_name
    lstm   = local.lstm_model_name
  }
}

output "validation_metrics" {
  description = "Calculated validation metrics"
  value = {
    accuracy = local.accuracy_score
    mse      = local.mse_score
    mae      = local.mae_score
  }
}

# Complete Infrastructure Summary
output "ml_infrastructure_summary" {
  description = "Complete ML infrastructure overview"
  value = {
    datasets = {
      count = 3
      total_rows = (
        ml_dataset.imagenet_subset.row_count +
        ml_dataset.sentiment_analysis.row_count +
        ml_dataset.stock_prices.row_count
      )
      total_size_gb = (
        ml_dataset.imagenet_subset.size_bytes +
        ml_dataset.sentiment_analysis.size_bytes +
        ml_dataset.stock_prices.size_bytes
      ) / 1024 / 1024 / 1024
    }
    models = {
      count = 3
      total_parameters = (
        ml_model.resnet50_classifier.parameter_count +
        ml_model.bert_sentiment.parameter_count +
        ml_model.lstm_forecaster.parameter_count
      )
      frameworks = ["pytorch", "pytorch", "tensorflow"]
    }
    training_jobs = {
      count        = 3 + length(ml_training_job.resnet_hp_tuning)
      total_epochs = (
        ml_training_job.train_resnet.epochs +
        ml_training_job.train_bert.epochs +
        ml_training_job.train_lstm.epochs
      )
      total_gpus = (
        ml_training_job.train_resnet.num_gpus +
        ml_training_job.train_bert.num_gpus +
        ml_training_job.train_lstm.num_gpus
      )
    }
    registry = {
      production_models = data.ml_model_registry.production_models.count
      staging_models    = data.ml_model_registry.staging_models.count
    }
    cost_estimate = {
      training_cost_usd    = local.estimated_training_cost
      total_training_hours = local.total_training_time_hours
    }
  }
}
