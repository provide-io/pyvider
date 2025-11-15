terraform {
  required_providers {
    pyvider = {
      source = "local/providers/pyvider"
    }
  }
}

provider "pyvider" {}

# Test format_tags function (using s_function!)
output "test_format_tags" {
  value = provider::pyvider::format_tags({
    Environment = "production"
    Project     = "s_function_test"
    Team        = "platform"
  }, true)
}

# Test calculate_cost function (using s_function!)
output "test_calculate_cost" {
  value = provider::pyvider::calculate_cost("t2.medium", 730)
}

# Test validate_cidr function (using s_function!)
output "test_validate_cidr_valid" {
  value = provider::pyvider::validate_cidr("10.0.0.0/16")
}

output "test_validate_cidr_invalid" {
  value = provider::pyvider::validate_cidr("not-a-cidr")
}

# Test generate_name function (using s_function!)
output "test_generate_name" {
  value = provider::pyvider::generate_name("web", "prod", "us-east-1", 42)
}
