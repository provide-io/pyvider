## 📜 The Magic Words: Configuration

Now that we have our provider installed, it's time to learn the magic words that will bring it to life. We'll start by configuring the provider in our Terraform configuration file.

Create a new file called `main.tf` and add the following:

```terraform
terraform {
  required_providers {
    "my-provider" = {
      source  = "local/providers/my-provider"
      version = "0.1.0"
    }
  }
}

provider "my-provider" {
  # Our journey begins here...
}
```

This tells Terraform that we want to use our custom provider. Now, let's add some real configuration.

## 🔑 Unlocking the Gates: Authentication

Most providers need to authenticate with an external API or service. `pyvider` provides a capability system that makes it easy to add authentication to your provider. We'll learn more about capabilities in a later chapter, but for now, let's assume our provider needs an API key.

We can add the API key to our provider configuration like this:

```terraform
provider "my-provider" {
  api_key = "my-super-secret-api-key"
}
```

And with that, we've unlocked the gates to our provider's power. In the next section, we'll learn how to create our first resource.
