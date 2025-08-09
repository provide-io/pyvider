# 🐛 Debugging

This guide provides tips and tricks for debugging your `pyvider` provider.

## 📄 Overview

Debugging `pyvider` providers can be tricky, but there are a few tools and techniques that can help.

## 🚀 Using the Debugger

You can use the `pdb` debugger to debug your provider. To do this, you'll need to set the `TF_REATTACH_PROVIDERS` environment variable to `true`. This will prevent Terraform from killing the provider process when it's finished.

```bash
export TF_REATTACH_PROVIDERS=true
```

You can then attach to the provider process with `pdb`:

```bash
python -m pdb -p <pid>
```

## 📝 Logging

You can use the logging system to get more information about what's happening in your provider. See the [Logging](./10-logging.md) documentation for more information.

## 🔬 Tracing

You can use a tool like `strace` or `dtruss` to trace the system calls that your provider is making. This can be useful for debugging low-level issues.
```
