# ✍️ The `file_content` Resource

Now, let's create the `file_content` resource.

## 📄 The Schema

First, let's define the schema for our resource. Create a new file called `resources/file_content.py` and add the following code:

```python
from pyvider.resources import resource, ResourceConfig

@resource
class FileContent(ResourceConfig):
    """
    Manages the content of a file on the local filesystem.
    """
    path: str
    content: str
```

In this schema, we define a resource named `FileContent` with two string attributes: `path` and `content`.

## 🧠 The Logic

Now, let's implement the logic for our resource.

```python
from pathlib import Path
from pyvider.resources import resource, ResourceConfig

@resource
class FileContent(ResourceConfig):
    """
    Manages the content of a file on the local filesystem.
    """
    path: str
    content: str

    def create(self, ctx):
        Path(self.path).write_text(self.content)
        ctx.state["id"] = self.path

    def read(self, ctx):
        try:
            content = Path(self.path).read_text()
            ctx.state["content"] = content
        except FileNotFoundError:
            ctx.state = {}

    def update(self, ctx):
        Path(self.path).write_text(self.content)

    def delete(self, ctx):
        Path(self.path).unlink()
```

And with that, we've created our `file_content` resource! In the next section, we'll learn how to test our new component.
```
