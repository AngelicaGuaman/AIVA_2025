import pytest
import numpy as np
from patrolscan import PatrolScan, Config
from PIL import Image
import io
import base64
import os

IMAGEN_TEST_PATH = "ImagenTest8966LFF.png"

# Fixtures reutilizables
@pytest.fixture
def scanner():
    config = Config()
    config.modelo_detector_path = "license_plate_detector.onnx"
    return PatrolScan(config)

@pytest.fixture
def imagen_prueba_bytes():
    # Cargar la imagen de prueba
    imagen_path = IMAGEN_TEST_PATH
    with open(imagen_path, 'rb') as f:
        imagen_bytes = f.read()
    return imagen_bytes

@pytest.fixture
def imagen_prueba_base64(imagen_prueba_bytes):
    return base64.b64encode(imagen_prueba_bytes).decode('utf-8')

@pytest.fixture
def imagen_prueba_numpy():
    # Cargar la imagen de prueba
    imagen_path = IMAGEN_TEST_PATH
    imagen = np.array(Image.open(imagen_path))
    return imagen

def test_patrolscan_initialization(scanner):
    assert scanner is not None
    assert scanner.detector is not None
    assert scanner.ocr is not None

@pytest.mark.parametrize("metodo,imagen_fixture", [
    ("scan_bytes", "imagen_prueba_bytes"),
    ("scan_base64", "imagen_prueba_base64"),
    ("scan_numpy_array", "imagen_prueba_numpy")
])
def test_single_scan_methods(scanner, metodo, imagen_fixture, request):
    """Test parametrizado para todos los métodos de escaneo individual"""
    imagen = request.getfixturevalue(imagen_fixture)
    metodo_func = getattr(scanner, metodo)
    result = metodo_func(imagen)
    
    assert result is not None
    assert isinstance(result, list)
    assert len(result) > 0
    # Verificar formato de resultados
    for matricula in result:
        assert isinstance(matricula, str)

@pytest.mark.parametrize("metodo,imagen_fixture", [
    ("batch_scan_bytes", "imagen_prueba_bytes"),
    ("batch_scan_base64", "imagen_prueba_base64"),
    ("batch_scan_numpy_array", "imagen_prueba_numpy")
])
def test_batch_scan_methods(scanner, metodo, imagen_fixture, request):
    """Test parametrizado para todos los métodos de escaneo por lotes"""
    imagen = request.getfixturevalue(imagen_fixture)
    metodo_func = getattr(scanner, metodo)
    
    # Para los métodos batch necesitamos una lista de imágenes
    if metodo == "batch_scan_numpy_array":
        imagenes = [
            imagen,
            np.ones((100, 100, 3), dtype=np.uint8)
        ]
    else:
        imagenes = [imagen, imagen]
        
    results = metodo_func(imagenes)
    
    assert results is not None
    assert isinstance(results, list)
    assert len(results) > 0
    # Verificar formato de resultados
    for matricula in results:
        assert isinstance(matricula, str)

def test_scan_bytes_invalid_input(scanner):
    """Prueba que se lance una excepción con entrada inválida"""
    with pytest.raises(ValueError, match="El tipo de datos no son bytes"):
        scanner.scan_bytes("esto no es bytes")

def test_scan_base64_invalid_input(scanner):
    """Prueba que se lance una excepción con entrada inválida"""
    with pytest.raises(ValueError, match="El tipo de datos no son string"):
        scanner.scan_base64(123)
        
def test_scan_numpy_array_invalid_input(scanner):
    """Prueba que se lance una excepción con entrada inválida"""
    with pytest.raises(ValueError, match="El tipo de datos no son numpy array"):
        scanner.scan_numpy_array("esto no es un array")

def test_funcional_reocnocimiento(scanner):
    """Test con una imagen real de una matrícula conocida"""
    
    # Ruta a la imagen de prueba real
    imagen_path = IMAGEN_TEST_PATH
    
    # Verificar que la imagen existe
    assert os.path.exists(imagen_path), f"La imagen de prueba no existe en: {imagen_path}"
    
    # Cargar la imagen como bytes
    with open(imagen_path, 'rb') as f:
        imagen_bytes = f.read()
    
    # Ejecutar el reconocimiento
    resultado = scanner.scan_bytes(imagen_bytes)
    
    # Verificar que la matrícula esperada está en los resultados
    assert "8966LFF" in resultado, f"La matrícula esperada no fue detectada. Resultados: {resultado}"
