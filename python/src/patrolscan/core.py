import base64
import numpy as np
import io
from PIL import Image
from patrolscan.utils import is_valid_license_plate, obtener_recortes_imagenes, preprocess_for_easyocr
from patrolscan.config import Config

class PatrolScan:
    def __init__(self, config=None):
        self.config = config or Config()
        self._init_modules()

    def _init_modules(self):
        """Inicializa los módulos principales"""
        from patrolscan.detector import Detector
        from patrolscan.ocr import OCR
        
        self.detector = Detector(self.config.modelo_detector_path, self.config.providers_onnx, self.config.conf_threshold_detector, self.config.iou_threshold_detector)
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

        lista_listas_zonas_detectadas = self.detector.detect(lista_image_numpy_array)

        lista_matriculas_detectadas = []
        for i, lista_zonas_detectadas in enumerate(lista_listas_zonas_detectadas):
            lista_recortes_imagenes = obtener_recortes_imagenes(lista_zonas_detectadas, lista_image_numpy_array[i])
            for recorte_imagen in lista_recortes_imagenes:
                # preprocessed_easyocr = preprocess_for_easyocr(recorte_imagen)
                texto_extraido = self.ocr.extract_text(recorte_imagen)
                if is_valid_license_plate(texto_extraido):
                    lista_matriculas_detectadas.append(texto_extraido)

        return lista_matriculas_detectadas


if __name__ == "__main__":
    import sys
    import os
    import argparse

    parser = argparse.ArgumentParser(description="Procesar imágenes o videos con PatrolScan.")
    parser.add_argument("--model", required=True, help="Ruta al modelo del detector.")
    parser.add_argument("--image", help="Ruta a la imagen a procesar.")
    parser.add_argument("--video", help="Ruta al video a procesar.")

    args = parser.parse_args()

    model_path = args.model
    image_path = args.image
    video_path = args.video

    #image_path = "src/patrolscan/data/ejemplo1.png"

    #config = {
    #'modelo_detector_path': model_path,
    #'providers_onnx': ['CPUExecutionProvider'],
    #'conf_threshold_detector': 0.5,
    #'iou_threshold_detector': 0.45
    #}

    config = Config()
    config.modelo_detector_path = model_path
    config.providers_onnx = ['CPUExecutionProvider']
    config.conf_threshold_detector = 0.5
    config.iou_threshold_detector = 0.45

    patrolscan = PatrolScan(config=config)

    #image_path = "src/patrolscan/data/ejemplo1.png"
    
    import cv2

    if(image_path is not None):
        image_numpy_array = cv2.imread(image_path)

        if image_numpy_array is None:
            raise FileNotFoundError(f"No se pudo cargar la imagen desde la ruta: {image_path}")
        
        result = patrolscan.scan_numpy_array(image_numpy_array)
        print(result)
    else:
        # It is video
        video = cv2.VideoCapture(video_path)
        if not video.isOpened():
            raise FileNotFoundError(f"No se pudo abrir el video desde la ruta: {video_path}")

        while True:
            ret, frame = video.read()
            if not ret:
                break

            frame_rate = int(video.get(cv2.CAP_PROP_FPS))
            frame_interval = max(1, frame_rate // 2)  # Process every second frame

            # Skip frames to slow down processing
            for _ in range(frame_interval - 1):
                ret, _ = video.read()
                if not ret:
                    break

            # Collect 10 frames to pass to PatrolScan
            frames_batch = []
            for _ in range(10):
                ret, frame = video.read()
                if not ret:
                    break
                frames_batch.append(frame)
            
            if len(frames_batch) > 0:
                result = patrolscan.batch_scan_numpy_array(frames_batch)
                print(result)

        video.release()
        cv2.destroyAllWindows()
