"""
PatrolScan - Sistema de detección y reconocimiento de matrículas
"""

from . import utils
from . import detector
from . import ocr
from .core import PatrolScan
from .config import Config

__all__ = [
    'detector',
    'ocr',
    'utils',
    'PatrolScan',
    'Config'
]
