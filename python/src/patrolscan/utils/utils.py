

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

def is_valid_license_plate(license_plate):
    """
    Simula la validación de una matrícula
    
    Args:
        license_plate (str): Matrícula a validar
    """
    return True