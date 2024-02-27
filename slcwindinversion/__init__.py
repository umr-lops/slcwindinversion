"""Top-level package for slcwindinversion."""

__author__ = """Antoine GROUAZEL"""
__email__ = 'antoine.grouazel@ifremer.fr'
from slcwindinversion import *
from importlib.metadata import version
try:
    __version__ = version("slcwindinversion")
except Exception:
    print('impossible to get version of slcwindinversion ')
    __version__ = "999"
