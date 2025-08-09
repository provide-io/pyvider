# 🪵 Logging

This guide explains how to use the logging system in your `pyvider` provider.

## 📄 Overview

`pyvider` uses the `structlog` library for logging. This library provides a powerful and flexible logging system that allows you to create structured logs.

## 🚀 Basic Example

Here is a basic example of how to use the logging system in your provider:

```python
from pyvider.telemetry import logger

def my_function():
    logger.info("This is my log message.")
```

In this example, we log an informational message to the console.

## ⚙️ Log Levels

The following log levels are available:

-   `debug`: Detailed information, typically of interest only when diagnosing problems.
-   `info`: Confirmation that things are working as expected.
-   `warning`: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
-   `error`: Due to a more serious problem, the software has not been able to perform some function.
-   `critical`: A serious error, indicating that the program itself may be unable to continue running.

## 📝 Structured Logging

You can use the `bind` method to add structured data to your logs.

```python
from pyvider.telemetry import logger

def my_function():
    log = logger.bind(user_id=123)
    log.info("This is my log message.")
```

In this example, we bind the `user_id` to the logger. This will add a `user_id=123` field to all the logs that are created with this logger.
```
