terraform {
  required_providers {
    pyvider = {
      source = "local/providers/pyvider"
      version = "0.1.0"
    }
  }
}

provider "pyvider" {
  # Provider configuration (empty for now)
}

# Test resource: Create a file with content
resource "pyvider_file_content" "test_file" {
  filename = "/tmp/pyvider_test.txt"
  content  = "Hello from Pyvider! The multi-provider architecture is working."
}

# Test data source: Read environment variables
data "pyvider_env_variables" "env" {
  filter_prefix = "PATH"
}

# Test function: String manipulation
output "test_function" {
  value = provider::pyvider::upper("hello world")
}

output "file_path" {
  value = pyvider_file_content.test_file.filename
}

output "env_path" {
  value = try(data.pyvider_env_variables.env.variables["PATH"], "PATH not found")
}