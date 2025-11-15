terraform {
  required_providers {
    demo = {
      source = "local/demo"
      version = "1.0.0"
    }
  }
}

provider "demo" {
  api_key = "test-key"
}

resource "demo_resource" "test" {
  name        = "test-resource"
  description = "Testing s_function with real Terraform"
  count       = 5
}

# Test the upper function (using s_function!)
output "test_upper" {
  value = provider::demo::upper("hello from terraform")
}

# Test the join_strings function (using s_function!)
output "test_join" {
  value = provider::demo::join_strings(["terraform", "pyvider", "s_function"], " + ")
}

# Test the add function (using s_function!)
output "test_add" {
  value = provider::demo::add(42, 58)
}
