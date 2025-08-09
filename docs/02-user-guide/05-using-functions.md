## 🧙‍♂️ Weaving Spells: The Function

Sometimes, we need to perform custom logic that is not possible with the built-in Terraform functions. This is where `pyvider` functions come in. Functions are like spells that we can cast to perform calculations, transformations, and other magical feats.

In this example, we'll create a function that converts a string to uppercase. Add the following to your `main.tf` file:

```terraform
output "uppercase_hello" {
  value = my-provider_upper("hello, pyvider!")
}
```

This tells Terraform that we want to call a function named `my-provider_upper` with the input `"hello, pyvider!"`.

Now, run `terraform apply` to call the function:

```bash
terraform apply
```

Terraform will show you the uppercase version of the string as an output variable.

And with that, you've woven your first spell and performed a magical transformation! In the next section, we'll learn how to put all the pieces together to create a truly powerful provider.
