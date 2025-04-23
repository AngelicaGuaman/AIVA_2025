import cv2

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
    Valida la matrícula según el formato español (4 dígitos + 3 letras),
    o (1 letra + 4 dígitos + 3 letras) para matrículas históricas, de remolque, etc.
    Args:
        license_plate (str): Matrícula a validar
        verbose (bool): Si es True, imprime mensajes detallados
    """
    
    if len(license_plate) != 7 and len(license_plate) != 8:
        if verbose:
            print(f"License plate '{license_plate}' is invalid: must be 7 characters long.")
        return False

    if len(license_plate) == 7:
        if verbose:
            print(f"Taxis, VTC, regular license plate format detected.")
        
        if not license_plate[:4].isdigit():
            if verbose:
                print(f"License plate '{license_plate}' is invalid: first 4 characters must be digits.")
            return False
        if not license_plate[4:].isalpha():
            if verbose:
                print(f"License plate '{license_plate}' is invalid: last 3 characters must be letters.")
            return False
        if not license_plate[4:].isupper():
            if verbose:
                print(f"License plate '{license_plate}' is invalid: last 3 characters must be uppercase letters.")
            return False
    
    if len(license_plate) == 8:
        if verbose:
            print(f"License plate format detected: trailers, historical, state forces, etc.")

        if not (license_plate[0].isalpha() and license_plate[0].isupper() and 
                license_plate[1:5].isdigit() and 
                license_plate[5:8].isalpha() and license_plate[5:8].isupper()):
            if verbose:
                print(f"License plate '{license_plate}' is invalid: first character must be an uppercase letter, next 4 characters must be digits, and last 3 characters must be uppercase letters.")
            return False


    if verbose:
        print(f"License plate '{license_plate}' is valid")
    return True