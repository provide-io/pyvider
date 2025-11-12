# Demo Provider Example Terraform Configuration
#
# This example demonstrates all features of the demo provider:
# - Provider configuration
# - Resource management
# - Data sources
# - Provider functions

terraform {
  required_providers {
    demo = {
      source = "local/provide/demo"
      version = "1.0.0"
    }
  }
}

# Configure the demo provider
provider "demo" {
  api_url   = "https://api.demo.example.com"
  timeout   = 30
  debug     = true
  # api_token = var.demo_api_token  # Use variable for sensitive data
}

# Create a demo server resource
resource "demo_server" "web" {
  name          = "web-server-01"
  instance_type = "t2.small"
  region        = "us-east-1"

  tags = {
    Environment = "production"
    Team        = "platform"
    ManagedBy   = "terraform"
  }

  enable_monitoring = true
}

# Create another server
resource "demo_server" "app" {
  name          = "app-server-01"
  instance_type = "t2.medium"
  region        = "us-west-2"

  tags = {
    Environment = "production"
    Team        = "backend"
    ManagedBy   = "terraform"
  }

  enable_monitoring = false
}

# Query server information using data source
data "demo_server_info" "web_info" {
  server_id = demo_server.web.id
}

# Use provider functions
locals {
  # Format tags as JSON
  web_tags_json = provider::demo::format_tags(demo_server.web.tags, true)

  # Calculate estimated monthly cost
  web_monthly_cost = provider::demo::calculate_cost(
    demo_server.web.instance_type,
    730  # Hours per month (24 * 30.4)
  )

  app_monthly_cost = provider::demo::calculate_cost(
    demo_server.app.instance_type,
    730
  )

  total_monthly_cost = local.web_monthly_cost + local.app_monthly_cost
}

# Outputs
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

output "web_tags_formatted" {
  description = "Web server tags as JSON"
  value       = local.web_tags_json
}

output "estimated_monthly_cost" {
  description = "Estimated monthly cost for all servers"
  value       = "$${local.total_monthly_cost}"
}

output "app_server_id" {
  description = "App server ID"
  value       = demo_server.app.id
}

output "app_server_public_ip" {
  description = "App server public IP"
  value       = demo_server.app.public_ip
}
