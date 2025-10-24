# 🚀 Advanced Usage

This guide provides advanced examples of how to use `pyvider`.

## `depends_on`

The `depends_on` meta-argument is used to create explicit dependencies between resources. This is useful when you have a resource that depends on another resource, but there is no explicit reference to the other resource in the configuration.

```terraform
resource "pyvider_null_resource" "a" {
}

resource "pyvider_null_resource" "b" {
  depends_on = [pyvider_null_resource.a]
}
```

In this example, the `pyvider_null_resource` `b` depends on the `pyvider_null_resource` `a`. This means that `a` will be created before `b`.

## `count`

The `count` meta-argument is used to create multiple instances of a resource.

```terraform
resource "pyvider_null_resource" "example" {
  count = 3
}
```

In this example, three instances of the `pyvider_null_resource` will be created.

## `for_each`

The `for_each` meta-argument is used to create multiple instances of a resource based on a map or a set of strings.

```terraform
resource "pyvider_null_resource" "example" {
  for_each = toset(["a", "b", "c"])
}
```

In this example, three instances of the `pyvider_null_resource` will be created, one for each element in the set.
```
