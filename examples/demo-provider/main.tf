terraform {
  required_providers {
    pyvider = {
      source = "local/providers/pyvider"
    }
  }
}

provider "pyvider" {
  api_key = "test-key"
}

resource "demo_resource" "test" {
  provider    = pyvider
  name        = "test-resource"
  description = "Testing s_function with real Terraform"
  count       = 5
}

# Test the upper function (using s_function!)
output "test_upper" {
  value = provider::pyvider::upper("hello from terraform")
}

# Test the join_strings function (using s_function!)
output "test_join" {
  value = provider::pyvider::join_strings(["terraform", "pyvider", "s_function"], " + ")
}

# Test the add function (using s_function!)
output "test_add" {
  value = provider::pyvider::add(42, 58)
}
