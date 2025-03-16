import pytest
import numpy as np
from patrolscan.detector import Detector

@pytest.fixture
def detector():
    return Detector()

def test_detector_initialization(detector):
    assert detector.initialized

def test_detect_single_image(detector):
    """Test con una sola imagen"""
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    
    regions = detector.detect([image])
    
    assert isinstance(regions, list)
    assert len(regions) > 0
    
    for region in regions[0]:
        assert len(region) == 4
        assert all(isinstance(coord, float) for coord in region)

