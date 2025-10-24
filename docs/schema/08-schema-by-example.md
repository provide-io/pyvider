# 🗺️ Schema by Example

This guide will walk you through the process of building a complex schema from the ground up.

## 🚀 The Goal

Our goal is to create a schema for a resource that represents a web server. The web server will have the following attributes:

-   `name`: The name of the web server.
-   `port`: The port that the web server listens on.
-   `enabled`: A boolean indicating whether the web server is enabled.
-   `aliases`: A list of aliases for the web server.
-   `config`: A map of configuration options for the web server.

## 🏗️ The Blueprint: The Schema

Here is the `pyvider` schema for our web server resource:

```python
from pyvider.schema import Attribute, Block

schema = Block(
    name="my_web_server",
    attributes=[
        Attribute(
            name="name",
            type="string",
            required=True,
            description="The name of the web server.",
        ),
        Attribute(
            name="port",
            type="number",
            optional=True,
            default=80,
            description="The port that the web server listens on.",
        ),
        Attribute(
            name="enabled",
            type="bool",
            optional=True,
            default=True,
            description="A boolean indicating whether the web server is enabled.",
        ),
        Attribute(
            name="aliases",
            type="list",
            optional=True,
            description="A list of aliases for the web server.",
        ),
        Attribute(
            name="config",
            type="map",
            optional=True,
            description="A map of configuration options for the web server.",
        ),
    ],
)
```

##  Terraform Configuration (HCL)

Here is an example of how you would use our web server resource in a Terraform configuration:

```hcl
resource "my-provider_my-web-server" "example" {
  name    = "my-web-server"
  port    = 8080
  enabled = true
  aliases = ["www.example.com", "example.com"]
  config = {
    "timeout" = "30s"
    "max_connections" = "1024"
  }
}
```
```
