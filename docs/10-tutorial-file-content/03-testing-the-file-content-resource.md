# 🧪 Testing the `file_content` Resource

Now that we've created our `file_content` resource, it's time to test it.

## 📄 The Test Plan

We'll create a new test file called `tests/test_file_content.py` and add a test for the `file_content` resource.

## 🚀 The `file_content` Resource Test

Here is the test for the `file_content` resource:

```python
from my_provider.resources import FileContent

def test_file_content_resource(tmp_path):
    file_path = tmp_path / "hello.txt"

    # Create the resource
    resource = FileContent(
        path=str(file_path),
        content="Hello, Pyvider!",
    )
    resource.create(None)
    assert file_path.read_text() == "Hello, Pyvider!"

    # Read the resource
    resource.read(None)
    assert resource.content == "Hello, Pyvider!"

    # Update the resource
    resource.content = "Hello, World!"
    resource.update(None)
    assert file_path.read_text() == "Hello, World!"

    # Delete the resource
    resource.delete(None)
    assert not file_path.exists()
```

## 🏃‍♀️ Running the Tests

Now, let's run the tests:

```bash
pytest
```

And with that, we've tested our new component!

## 🎉 The Scribe's Masterpiece

Congratulations, scribe! You've successfully created a `pyvider` resource that can manage the content of a file on the local filesystem.

Now, go forth and write your own stories!
```
