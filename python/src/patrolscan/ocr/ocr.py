import easyocr

class OCR:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])
        self.initialized = True

    def extract_text(self, image_numpy_array):
        """
        Simula la extracción de texto de una imagen
        
        Args:
            image_numpy_array (numpy.ndarray): Numpy array que representa una imagen
            
        Returns:
            str: Texto extraído simulado
        """
        result = self.reader.readtext(image_numpy_array)
        #union de detecciones
        # Sorteamos por la esquina superior izquierda
        result.sort(key=lambda x: x[0][0][0])

        texto = ""
        for detection in result:
            texto += detection[1]
        texto = texto.replace(" ", "")
        return texto