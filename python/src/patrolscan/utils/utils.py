import cv2
import re

def obtener_recortes_imagenes(lista_zonas_detectadas, imagen_original):
    """
    Recorta las zonas detectadas de las imágenes
    """
    lista_recortes = []
    for zona_detectada in lista_zonas_detectadas:
        x1, y1, x2, y2 = zona_detectada
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        recorte = imagen_original[y1:y2, x1:x2]
        lista_recortes.append(recorte)
    return lista_recortes

def preprocess_for_easyocr(image):
    """
    Preprocesa la imagen para mejorar el reconocimiento con EasyOCR
    """
    # Redimensionar manteniendo el aspecto
    height, width = image.shape[:2]
    # Añadir un pequeño borde
    bordered = cv2.copyMakeBorder(image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    
    # Convertir a escala de grises para algunas operaciones
    gray = cv2.cvtColor(bordered, cv2.COLOR_BGR2GRAY)
    
    # Mejora de contraste
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    equalized = clahe.apply(gray)
    
    # Convertir de nuevo a BGR para EasyOCR (que acepta imágenes en color)
    equalized_bgr = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)
    
    return equalized_bgr

def is_valid_license_plate(license_plate, verbose=False):
    """
    Valida la matrícula según el formato español:
    - Formato regular: 4 dígitos + 3 letras (e.g., 1234ABC)
    - Formato especial (históricas, de remolque, etc): 1 letra + 4 dígitos + 3 letras (e.g., A1234BCD)
    
    Args:
        license_plate (str): Matrícula a validar
        verbose (bool): Si es True, imprime mensajes detallados
    
    Returns:
        bool: True si la matrícula es válida, False en caso contrario
    """
    # Definir patrones para los formatos de matrícula
    regular_pattern = r"^\d{4}[A-Z]{3}$"
    special_pattern = r"^[A-Z]{1}\d{4}[A-Z]{3}$"

    # Validar contra los patrones
    if re.match(regular_pattern, license_plate):
        if verbose:
            print(f"License plate '{license_plate}' is valid (regular format).")
        return True
    elif re.match(special_pattern, license_plate):
        if verbose:
            print(f"License plate '{license_plate}' is valid (special format).")
        return True
    else:
        if verbose:
            print(f"License plate '{license_plate}' is invalid.")
        return False
