terraform {
  required_providers {
    demo = {
      source = "local/providers/demo"
    }
  }
}

provider "demo" {}

# Test format_tags function (using s_function!)
output "test_format_tags" {
  value = provider::demo::format_tags({
    Environment = "production"
    Project     = "s_function_test"
    Team        = "platform"
  }, true)
}

# Test calculate_cost function (using s_function!)
output "test_calculate_cost" {
  value = provider::demo::calculate_cost("t2.medium", 730)
}

# Test validate_cidr function (using s_function!)
output "test_validate_cidr_valid" {
  value = provider::demo::validate_cidr("10.0.0.0/16")
}

output "test_validate_cidr_invalid" {
  value = provider::demo::validate_cidr("not-a-cidr")
}

# Test generate_name function (using s_function!)
output "test_generate_name" {
  value = provider::demo::generate_name("web", "prod", "us-east-1", 42)
}
