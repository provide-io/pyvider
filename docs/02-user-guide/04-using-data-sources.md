## 🔮 Peering into the Crystal Ball: The Data Source

Sometimes, we need to fetch information from the outside world to help us build our infrastructure. This is where data sources come in. Data sources are like read-only views of the world, and they allow us to fetch information from APIs, services, and devices.

In this example, we'll create a data source that reads the content of our `hello.txt` file. Add the following to your `main.tf` file:

```terraform
data "my-provider_my-file" "example" {
  path = "hello.txt"
}

output "file_content" {
  value = data.my-provider_my-file.example.content
}
```

This tells Terraform that we want to read data from a data source of type `my-provider_my-file` with the name `example`. We're also giving it one attribute: `path`.

Now, run `terraform apply` to read the data from the data source:

```bash
terraform apply
```

Terraform will show you the content of the `hello.txt` file as an output variable.

And with that, you've peered into the crystal ball and read data from the outside world! In the next section, we'll learn how to use functions to perform custom logic.
