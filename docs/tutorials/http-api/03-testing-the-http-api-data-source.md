# 🧪 Testing the `http_api` Data Source

Now that we've created our `http_api` data source, it's time to test it.

## 📄 The Test Plan

We'll create a new test file called `tests/test_http_api.py` and add a test for the `http_api` data source.

## 🚀 The `http_api` Data Source Test

Here is the test for the `http_api` data source:

```python
from my_provider.data_sources import HttpApi

def test_http_api_data_source(httpx_mock):
    httpx_mock.add_response(
        method="GET",
        url="https://example.com",
        text="Hello, Pyvider!",
    )

    data_source = HttpApi(
        url="https://example.com",
    )
    result = data_source.read(None)
    assert result["body"] == "Hello, Pyvider!"
```

## 🏃‍♀️ Running the Tests

Now, let's run the tests:

```bash
pytest
```

And with that, we've tested our new component!

## 🎉 The Oracle's Wisdom

Congratulations, seeker of knowledge! You've successfully created a `pyvider` data source that can consult the oracle and retrieve information from the web.

Now, go forth and use your newfound power to build amazing things!
```
