import pytest
import numpy as np
from patrolscan.ocr import OCR

@pytest.fixture
def ocr():
    return OCR()

def test_ocr_initialization(ocr):
    assert ocr.initialized

def test_extract_text_empty_image(ocr):
    """Test con imagen vacía"""
    result = ocr.extract_text(np.zeros((100, 100, 3), dtype=np.uint8))
    assert isinstance(result, str)
