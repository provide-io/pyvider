# 🧪 Testing the `jq` Components

Now that we've created our `jq` components, it's time to test them.

## 📄 The Test Plan

We'll create a new test file called `tests/test_jq.py` and add the following tests:

-   A test for the `jq` function.
-   A test for the `jq` data source.

## 🚀 The `jq` Function Test

Here is the test for the `jq` function:

```python
from my_provider.functions import jq

def test_jq_function():
    json_string = '{"foo": "bar"}'
    filter = ".foo"
    result = jq(json_string, filter)
    assert result == "bar"
```

## 📊 The `jq` Data Source Test

Here is the test for the `jq` data source:

```python
from my_provider.data_sources import Jq

def test_jq_data_source(tmp_path):
    json_file = tmp_path / "test.json"
    json_file.write_text('{"foo": "bar"}')

    data_source = Jq(
        path=str(json_file),
        filter=".foo",
    )
    result = data_source.read(None)
    assert result["result"] == "bar"
```

## 🏃‍♀️ Running the Tests

Now, let's run the tests:

```bash
pytest
```

And with that, we've tested our new components!

## 🎉 The Grand Finale

Congratulations, artisan! You've successfully created a real-world `pyvider` component from scratch. You've learned how to create a function and a data source, and how to test them.

Now, go forth and create your own amazing `pyvider` components! The world is your oyster.
```
