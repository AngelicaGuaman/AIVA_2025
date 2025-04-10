import pytest
import numpy as np
from patrolscan.ocr import OCR
from PIL import Image

IMAGEN_TEST_PATH = "matriculatest4971JBV.jpg"

@pytest.fixture
def ocr():
    return OCR()

@pytest.fixture
def imagen_prueba_numpy():
    # Cargar la imagen de prueba
    imagen_path = IMAGEN_TEST_PATH
    imagen = np.array(Image.open(imagen_path))
    return imagen

def test_ocr_initialization(ocr):
    assert ocr.initialized

def test_extract_text_image(ocr, imagen_prueba_numpy):
    """Test con imagen vacía"""
    result = ocr.extract_text(imagen_prueba_numpy)
    assert isinstance(result, str)
    assert result == "4971JBV"