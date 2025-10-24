## ✨ Creating Your First Masterpiece: The Resource

Now that we've configured our provider, it's time to create our first masterpiece: a resource. Resources are the heart of Terraform, and they represent the infrastructure objects that we want to manage.

In this example, we'll create a simple resource that represents a file on the local filesystem. Add the following to your `main.tf` file:

```terraform
resource "my-provider_my-file" "example" {
  path    = "hello.txt"
  content = "Hello, Pyvider!"
}
```

This tells Terraform that we want to create a new resource of type `my-provider_my-file` with the name `example`. We're also giving it two attributes: `path` and `content`.

Now, run `terraform apply` to create the resource:

```bash
terraform apply
```

Terraform will ask you to confirm that you want to create the resource. Type `yes` and press Enter.

And with that, you've created your first resource! You should now see a new file called `hello.txt` in your directory with the content "Hello, Pyvider!".

In the next section, we'll learn how to read data from a data source.
