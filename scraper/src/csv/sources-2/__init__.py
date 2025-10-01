"""
Package containing per-site source definitions.
Each module in this package should expose a variable named `SOURCE` which
is a dict containing the xpaths and settings used by the scraper.

This module dynamically imports available modules and exposes a list
`SOURCES` with all discovered SOURCE dicts.
"""
import pkgutil
import importlib
import inspect
import os

SOURCES = []

package_name = __name__
package_path = os.path.dirname(__file__)

for finder, name, ispkg in pkgutil.iter_modules([package_path]):
    if name in ("__pycache__",):
        continue
    module = importlib.import_module(f"{package_name}.{name}")
    # if module exports SOURCE, add it
    if hasattr(module, "SOURCE") and isinstance(getattr(module, "SOURCE"), dict):
        SOURCES.append(getattr(module, "SOURCE"))
