terraform {
  required_providers {
    pyvider = {
      source = "local/providers/pyvider"
    }
  }
}

provider "pyvider" {}

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
