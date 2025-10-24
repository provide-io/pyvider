# 🚀 Advanced Examples

This guide provides advanced examples of how to use `pyvider`.

## 🧩 Composing Resources and Functions

Here is an example of how to compose resources and functions to create a more complex infrastructure. You can find the full, testable example in the [`examples/04-advanced-composition`](../../../examples/04-advanced-composition) directory.

```terraform
resource "pyvider_file_content" "example" {
  path    = "hello.txt"
  content = pyvider_upper("hello world")
}

data "pyvider_file_info" "example" {
  path = pyvider_file_content.example.path
}

output "file_info" {
  value = data.pyvider_file_info.example
}
```

This example creates a new resource of type `pyvider_file_content` with the name `example`. The `content` attribute is set to the output of the `pyvider_upper` function. The output of the `pyvider_file_content` resource is then used to configure the `path` attribute of the `pyvider_file_info` data source.
