"""
PatrolScan - Sistema de detección y reconocimiento de matrículas
"""

from . import utils
from . import detector
from . import ocr
from .core import PatrolScan

__all__ = [
    'detector',
    'ocr',
    'utils',
    'PatrolScan'
]
