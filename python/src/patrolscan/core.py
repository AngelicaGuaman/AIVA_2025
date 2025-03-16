import base64
import numpy as np
import io
from PIL import Image
from patrolscan.utils import is_valid_license_plate


class PatrolScan:
    def __init__(self, config=None):
        self.config = config or {}
        self._init_modules()

    def _init_modules(self):
        """Inicializa los módulos principales"""
        from .detector import Detector
        from .ocr import OCR
        
        self.detector = Detector()
        self.ocr = OCR()

    def scan_bytes(self, image_bytes):
        """
        Simula el escaneo de una imagen en bytes y retorna resultados mock
        
        Args:
            image_bytes (bytes): Imagen en formato bytes
            
        Returns:
            dict: Resultados simulados del escaneo
        """
        # Comprobamos si el tipo de datos son bytes
        if not isinstance(image_bytes, bytes):
            raise ValueError("El tipo de datos no son bytes")
        
        # Convertir bytes a array numpy usando PIL
        image = Image.open(io.BytesIO(image_bytes))
        image_array = np.array(image)
        
        # Usar el método scan_numpy_array
        return self.scan_numpy_array(image_array)
    
    def scan_base64(self, image_base64):
        """
        Simula el escaneo de una imagen en formato base64 y retorna resultados mock
        
        Args:
            image_base64 (str): Cadena base64 que representa la imagen
        """
        # Comprobamos si el tipo de datos es string
        if not isinstance(image_base64, str):
            raise ValueError("El tipo de datos no son string")
        
        # Decodificar base64 a bytes
        image_bytes = base64.b64decode(image_base64)
        
        # Convertir bytes a array numpy usando PIL
        image = Image.open(io.BytesIO(image_bytes))
        image_array = np.array(image)
        
        # Usar el método scan_numpy_array
        return self.scan_numpy_array(image_array)
    
    def scan_numpy_array(self, image_numpy_array):
        """
        Simula el escaneo de una imagen y retorna resultados mock
        """
        # Comprobamos si el tipo de datos es numpy array
        if not isinstance(image_numpy_array, np.ndarray):
            raise ValueError("El tipo de datos no son numpy array")

        return self.__pipeline([image_numpy_array])


    def batch_scan_bytes(self, images_in_bytes):
        """
        Simula el procesamiento de múltiples imágenes
        
        Args:
            image_paths (list): Lista de rutas de imágenes
            
        Returns:
            list: Lista de resultados por imagen
        """
        # Comprobamos si el tipo de datos es lista de bytes
        if not isinstance(images_in_bytes, list):
            raise ValueError("El tipo de datos no son lista")
        
        for image_bytes in images_in_bytes:
            if not isinstance(image_bytes, bytes):
                raise ValueError("Algunos de los datos no son bytes")

        images_in_numpy_array = [np.array(Image.open(io.BytesIO(image_bytes))) for image_bytes in images_in_bytes]

        return self.__pipeline(images_in_numpy_array)
    

    def batch_scan_base64(self, images_in_base64):
        """
        Simula el procesamiento de múltiples imágenes en formato base64
        
        Args:
            images_in_base64 (list): Lista de cadenas base64 que representan imágenes
        
        Returns:
            list: Lista de resultados por imagen
        """
        # Comprobamos si el tipo de datos es lista de strings
        if not isinstance(images_in_base64, list):
            raise ValueError("El tipo de datos no son lista")
        
        for image_base64 in images_in_base64:
            if not isinstance(image_base64, str):
                raise ValueError("Algunos de los datos no son strings")

        images_in_bytes = [base64.b64decode(image_base64) for image_base64 in images_in_base64]
        return self.batch_scan_bytes(images_in_bytes)
    
    def batch_scan_numpy_array(self, images_in_numpy_array):
        """
        Simula el procesamiento de múltiples imágenes en formato numpy array
        
        Args:
            images_in_numpy_array (list): Lista de arrays numpy que representan imágenes
        
        Returns:
            list: Lista de resultados por imagen
        """
        # Comprobamos si el tipo de datos es lista de numpy arrays
        if not isinstance(images_in_numpy_array, list):
            raise ValueError("El tipo de datos no son lista")
        
        for image_numpy_array in images_in_numpy_array:
            if not isinstance(image_numpy_array, np.ndarray):
                raise ValueError("Algunos de los datos no son numpy arrays")
            
        return self.__pipeline(images_in_numpy_array)
    
    def __pipeline(self, lista_image_numpy_array):

        lista_imagenes_detectadas = self.detector.detect(lista_image_numpy_array)


        lista_matriculas_detectadas = []
        for zonas_detectadas in lista_imagenes_detectadas:
            for zona_detectada in zonas_detectadas:
                texto_extraido = self.ocr.extract_text(zona_detectada)
                if is_valid_license_plate(texto_extraido):
                    lista_matriculas_detectadas.append(texto_extraido)

        return lista_matriculas_detectadas


