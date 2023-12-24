"""Unofficial Chicago Transit Authority SDK for the BusTime API for Python.

https://www.ctabustracker.com/bustime/apidoc/docs/DeveloperAPIGuide3_0.pdf
"""
__title__ = "cta_bus"
__description__ = "Unofficial Chicago Transit Authority SDK for the BusTime API."
__version__ = "0.1.0"


from .client import Client


class CTA(Client):
    """Proxy class for Client."""
