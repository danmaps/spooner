"""Lightweight subset of :mod:`pkg_resources` for offline environments.

This project depends on ``pronouncing``/``cmudict`` which import
``pkg_resources.resource_stream`` and ``pkg_resources.resource_string`` to load
packaged data. In environments where ``setuptools`` (which provides
``pkg_resources``) is unavailable, importing ``pronouncing`` fails during test
collection. This shim supplies just the APIs needed by our dependencies using
:mod:`importlib.resources` so the package can function without the external
runtime dependency.
"""
from __future__ import annotations

import importlib.resources
from typing import BinaryIO


def resource_stream(package: str, resource_name: str) -> BinaryIO:
    """Return a binary stream for ``resource_name`` within ``package``.

    This mirrors the small portion of ``pkg_resources`` exercised by our
    dependencies and intentionally supports only file-like binary access.
    """

    return importlib.resources.files(package).joinpath(resource_name).open("rb")


def resource_string(package: str, resource_name: str) -> bytes:
    """Return the full contents of a packaged resource as bytes."""

    with resource_stream(package, resource_name) as stream:
        return stream.read()
