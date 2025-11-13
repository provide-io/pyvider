# Demo Provider - Comprehensive Example Terraform Configuration
#
# This example demonstrates ALL features of the demo provider:
# - 1 Provider configuration
# - 3 Resources (server, database, network)
# - 4 Data sources (server_info, regions, instance_types, account)
# - 4 Provider functions (format_tags, calculate_cost, validate_cidr, generate_name)

terraform {
  required_providers {
    demo = {
      source = "local/provide/demo"
      version = "1.0.0"
    }
  }
}

# ============================================================================
# Provider Configuration
# ============================================================================

provider "demo" {
  api_url   = "https://api.demo.example.com"
  timeout   = 30
  debug     = true
  # api_token = var.demo_api_token  # Use variable for sensitive data
}

# ============================================================================
# Data Sources - Query Available Options
# ============================================================================

# Query all available regions
data "demo_regions" "all" {}

# Query US regions only
data "demo_regions" "us" {
  filter_prefix = "us"
}

# Query all instance types
data "demo_instance_types" "all" {}

# Query t3 family instances with at least 2 vCPUs
data "demo_instance_types" "t3_large" {
  family     = "t3"
  min_vcpus  = 2
}

# ============================================================================
# Local Values - Using Provider Functions
# ============================================================================

locals {
  # Validate CIDR blocks
  vpc_cidr_valid = provider::demo::validate_cidr("10.0.0.0/16")
  subnet_cidr_valid = provider::demo::validate_cidr("10.0.1.0/24")
  invalid_cidr = provider::demo::validate_cidr("invalid")

  # Generate standardized names
  server_name = provider::demo::generate_name("web", "prod", "us-east-1", 1)
  db_name     = provider::demo::generate_name("db", "prod", "us-east-1", 1)

  # Common tags
  common_tags = {
    Environment = "production"
    Team        = "platform"
    ManagedBy   = "terraform"
    Project     = "demo"
  }

  # Format tags as JSON
  tags_json = provider::demo::format_tags(local.common_tags, true)
}

# ============================================================================
# Resource: Network (VPC)
# ============================================================================

resource "demo_network" "main" {
  name                 = "prod-vpc-main"
  cidr_block           = "10.0.0.0/16"
  enable_dns           = true
  enable_dns_hostnames = true

  subnets = [
    "10.0.1.0/24",  # Public subnet 1
    "10.0.2.0/24",  # Public subnet 2
    "10.0.10.0/24", # Private subnet 1
    "10.0.11.0/24", # Private subnet 2
  ]

  tags = merge(local.common_tags, {
    Name = "Production VPC"
    Type = "network"
  })
}

# ============================================================================
# Resource: Database
# ============================================================================

resource "demo_database" "main" {
  name          = local.db_name
  engine        = "postgresql"
  engine_version = "14.0"
  storage_gb    = 100
  instance_class = "db.t3.micro"

  backup_retention_days = 14
  multi_az             = true

  tags = merge(local.common_tags, {
    Name = "Production Database"
    Type = "database"
  })
}

# ============================================================================
# Resource: Servers
# ============================================================================

# Web server
resource "demo_server" "web" {
  name          = local.server_name
  instance_type = "t3.medium"
  region        = "us-east-1"

  tags = merge(local.common_tags, {
    Name = "Web Server"
    Role = "web"
  })

  enable_monitoring = true
}

# Application server
resource "demo_server" "app" {
  name          = provider::demo::generate_name("app", "prod", "us-east-1", 1)
  instance_type = "t3.large"
  region        = "us-east-1"

  tags = merge(local.common_tags, {
    Name = "Application Server"
    Role = "application"
  })

  enable_monitoring = true
}

# Backend API server
resource "demo_server" "api" {
  name          = provider::demo::generate_name("api", "prod", "us-west-2", 1)
  instance_type = "t3.medium"
  region        = "us-west-2"

  tags = merge(local.common_tags, {
    Name = "API Server"
    Role = "api"
  })

  enable_monitoring = false
}

# ============================================================================
# Data Source: Query Server Information
# ============================================================================

data "demo_server_info" "web_info" {
  server_id = demo_server.web.id
}

data "demo_server_info" "app_info" {
  server_id = demo_server.app.id
}

# ============================================================================
# Locals: Cost Calculations
# ============================================================================

locals {
  # Calculate monthly costs for each server (730 hours/month)
  web_monthly_cost = provider::demo::calculate_cost(
    demo_server.web.instance_type,
    730
  )

  app_monthly_cost = provider::demo::calculate_cost(
    demo_server.app.instance_type,
    730
  )

  api_monthly_cost = provider::demo::calculate_cost(
    demo_server.api.instance_type,
    730
  )

  # Total infrastructure cost
  total_monthly_cost = (
    local.web_monthly_cost +
    local.app_monthly_cost +
    local.api_monthly_cost
  )

  # Annual cost projection
  annual_cost = local.total_monthly_cost * 12
}

# ============================================================================
# Outputs: Infrastructure Information
# ============================================================================

# Network Outputs
output "vpc_id" {
  description = "VPC ID"
  value       = demo_network.main.vpc_id
}

output "vpc_cidr" {
  description = "VPC CIDR block"
  value       = demo_network.main.cidr_block
}

output "vpc_subnets" {
  description = "VPC subnet CIDR blocks"
  value       = demo_network.main.subnets
}

# Database Outputs
output "database_id" {
  description = "Database ID"
  value       = demo_database.main.id
}

output "database_endpoint" {
  description = "Database connection endpoint"
  value       = demo_database.main.endpoint
}

output "database_port" {
  description = "Database connection port"
  value       = demo_database.main.port
}

# Server Outputs
output "web_server_id" {
  description = "Web server ID"
  value       = demo_server.web.id
}

output "web_server_public_ip" {
  description = "Web server public IP"
  value       = demo_server.web.public_ip
}

output "web_server_status" {
  description = "Web server status"
  value       = data.demo_server_info.web_info.status
}

output "web_server_uptime" {
  description = "Web server uptime in seconds"
  value       = data.demo_server_info.web_info.uptime_seconds
}

output "app_server_id" {
  description = "Application server ID"
  value       = demo_server.app.id
}

output "app_server_public_ip" {
  description = "Application server public IP"
  value       = demo_server.app.public_ip
}

output "api_server_id" {
  description = "API server ID"
  value       = demo_server.api.id
}

output "api_server_public_ip" {
  description = "API server public IP"
  value       = demo_server.api.public_ip
}

# Region Outputs
output "all_regions" {
  description = "All available regions"
  value       = data.demo_regions.all.regions
}

output "us_regions" {
  description = "US regions only"
  value       = data.demo_regions.us.regions
}

output "region_count" {
  description = "Total number of available regions"
  value       = data.demo_regions.all.count
}

# Instance Type Outputs
output "all_instance_types" {
  description = "All available instance types"
  value       = data.demo_instance_types.all.instance_types
}

output "t3_instance_types" {
  description = "T3 family instance types with 2+ vCPUs"
  value       = data.demo_instance_types.t3_large.instance_types
}

# Validation Outputs
output "cidr_validation" {
  description = "CIDR block validation results"
  value = {
    vpc_cidr_valid    = local.vpc_cidr_valid
    subnet_cidr_valid = local.subnet_cidr_valid
    invalid_cidr      = local.invalid_cidr
  }
}

# Generated Names Output
output "generated_names" {
  description = "Generated standardized resource names"
  value = {
    server_name = local.server_name
    db_name     = local.db_name
  }
}

# Tags Output
output "tags_formatted" {
  description = "Common tags formatted as JSON"
  value       = local.tags_json
}

# Cost Outputs
output "monthly_costs" {
  description = "Monthly cost breakdown"
  value = {
    web_server = "$${format("%.2f", local.web_monthly_cost)}"
    app_server = "$${format("%.2f", local.app_monthly_cost)}"
    api_server = "$${format("%.2f", local.api_monthly_cost)}"
    total      = "$${format("%.2f", local.total_monthly_cost)}"
  }
}

output "annual_cost_projection" {
  description = "Estimated annual infrastructure cost"
  value       = "$${format("%.2f", local.annual_cost)}"
}

# Summary Output
output "infrastructure_summary" {
  description = "Complete infrastructure summary"
  value = {
    network = {
      vpc_id     = demo_network.main.vpc_id
      cidr_block = demo_network.main.cidr_block
      subnets    = length(demo_network.main.subnets)
    }
    database = {
      id       = demo_database.main.id
      engine   = demo_database.main.engine
      endpoint = demo_database.main.endpoint
      multi_az = demo_database.main.multi_az
    }
    servers = {
      web = {
        id        = demo_server.web.id
        type      = demo_server.web.instance_type
        public_ip = demo_server.web.public_ip
        uptime    = data.demo_server_info.web_info.uptime_seconds
      }
      app = {
        id        = demo_server.app.id
        type      = demo_server.app.instance_type
        public_ip = demo_server.app.public_ip
        uptime    = data.demo_server_info.app_info.uptime_seconds
      }
      api = {
        id        = demo_server.api.id
        type      = demo_server.api.instance_type
        public_ip = demo_server.api.public_ip
      }
    }
    costs = {
      monthly = format("$%.2f", local.total_monthly_cost)
      annual  = format("$%.2f", local.annual_cost)
    }
    metadata = {
      regions_available = data.demo_regions.all.count
      instance_types    = data.demo_instance_types.all.count
    }
  }
}
