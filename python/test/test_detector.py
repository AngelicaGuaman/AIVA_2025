import pytest
import numpy as np
from patrolscan.detector import Detector
from patrolscan.config import Config
from PIL import Image

IMAGEN_TEST_PATH = "ImagenTest8966LFF.png"

@pytest.fixture
def detector():
    return Detector(model_path="license_plate_detector.onnx")

@pytest.fixture
def imagen_prueba_numpy():
    # Cargar la imagen de prueba
    imagen_path = IMAGEN_TEST_PATH
    imagen = np.array(Image.open(imagen_path))
    return imagen

def test_detector_initialization(detector):
    assert detector.initialized

def test_detect_single_image(detector, imagen_prueba_numpy):
    """Test con una sola imagen"""

    image = imagen_prueba_numpy
    
    regions = detector.detect([image])
    
    assert isinstance(regions, list)
    assert len(regions) > 0
    
    for region in regions[0]:
        assert len(region) == 4
        for coord in region:
            assert isinstance(coord, (float)), f"La coordenada {coord} no es un número"
