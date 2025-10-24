# Chapter 2: The Journey Begins - Your First Pyvider Provider

Welcome, adventurer, to the exciting world of `pyvider`! In this chapter, we'll embark on a journey to build your very first `pyvider` provider. We'll start with the basics and gradually build up to a fully functional provider that can manage real infrastructure.

## 🎒 Preparing for the Journey

Before we begin, we need to make sure we have the right tools for the job. You'll need:

*   **Python 3.11 or later:** `pyvider` requires Python 3.11 or newer.
*   **Terraform 1.0 or later:** You'll need Terraform to use your `pyvider` provider.

## 🚀 The First Step: Installation

The first step on our journey is to install `pyvider`. You can do this using `pip`:

```bash
pip install pyvider
```

## 🏡 Building Your Workshop: The Provider Project

Now that we have `pyvider` installed, it's time to build our workshop. We'll create a new provider project using the `pyvider` command-line tool:

```bash
pyvider new my-provider
```

This will create a new directory called `my-provider` with a basic provider project structure. This is where we'll be doing all our work.

## 🛠️ Forging the Tools: Installing the Provider

Before we can use our provider, we need to forge it. We'll build the provider using the `pyvider` command-line tool:

```bash
cd my-provider
pyvider build
```

This will create a binary file in the `dist` directory. This is our provider, ready to be used.

Now, we need to install the provider so that Terraform can find it. We'll do this by copying the provider binary to the Terraform plugins directory:

```bash
mkdir -p ~/.terraform.d/plugins/local/providers/my-provider/0.1.0/linux_amd64
cp dist/terraform-provider-my-provider ~/.terraform.d/plugins/local/providers/my-provider/0.1.0/linux_amd64/
```

And with that, we're ready to start building our first resource!
