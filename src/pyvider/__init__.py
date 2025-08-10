# pyvider/__init__.py (namespace package)
# This file declares 'pyvider' as a namespace package, allowing it to be
# extended across multiple directories (like src/pyvider and components/).
# It should not contain any application logic or imports that could cause cycles.

__path__ = __import__("pkgutil").extend_path(__path__, __name__)
