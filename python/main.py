import sys
import onnxruntime as ort
import cv2
import numpy as np
import easyocr
import time
 
class LicensePlateDetector:
    def __init__(self, model_path="license_plate_detector.onnx"):
        """
        Inicializa el detector de matrículas usando ONNX Runtime con CPU
        """
        # Configurar opciones para usar solo CPU
        providers = ['CPUExecutionProvider']
        self.session = ort.InferenceSession(model_path, providers=providers)
        
        # Obtener nombres de entrada/salida del modelo
        self.input_name = self.session.get_inputs()[0].name
        self.output_names = [output.name for output in self.session.get_outputs()]
 
    def preprocess_image(self, image_path):
        """
        Preprocesa la imagen para el modelo ONNX
        """
        if isinstance(image_path, str):
            image = cv2.imread(image_path)
        else:
            image = image_path
            
        # Redimensionar y preparar la imagen (ajustar según tu modelo)
        input_height, input_width = 640, 640
        img = cv2.resize(image, (input_width, input_height))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Normalizar y cambiar formato
        img = img.astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1))  # HWC -> CHW
        img = np.expand_dims(img, axis=0)  # Añadir dimensión del batch
        print(img.shape)
        
        return img, image
    
    def non_max_suppression(self, detections, iou_threshold=0.45):
        """
        Aplica Non-Maximum Suppression a las detecciones
        """
        # Si no hay detecciones, devolver un array vacío
        if len(detections) == 0:
            return np.array([])
        
        # Extraer coordenadas y confianzas
        x1 = detections[:, 0]
        y1 = detections[:, 1]
        x2 = detections[:, 2]
        y2 = detections[:, 3]
        boxes = np.column_stack((x1, y1, x2, y2))
        scores = detections[:, 4]
        scores = scores.flatten()
 
        # Apply non-maximum suppression
        indices = cv2.dnn.NMSBoxes(bboxes=boxes, scores=scores, score_threshold=0.7, nms_threshold=0.45)
        # Filter out the boxes based on the NMS result
        filtered_boxes = [boxes[i] for i in indices.flatten()]
        
        # Devolver las detecciones filtradas
        return filtered_boxes
 
    def detect(self, image_path, conf_threshold=0.5):
        """
        Detecta matrículas en la imagen
        """
        # Preprocesar imagen
        input_tensor, original_image = self.preprocess_image(image_path)
        
        original_shape = original_image.shape
 
        # Inferencia
        outputs = self.session.run(self.output_names, {self.input_name: input_tensor})
        
        # Procesar resultados (ajustar según la salida de tu modelo)
        # Asumiendo que la salida tiene el formato [batch, num_detections, 6]
        # donde 6 = [x1, y1, x2, y2, confidence, class]
        detections = np.transpose(outputs[0])
        
        # Filtrar por confianza
        boxes = []
        mask = detections[:, 4] >= conf_threshold
        for i, booleana in enumerate(mask):
            if booleana:
                x, y, w, h = detections[i, :4]
                x1 = ((x - w/2) / 640) * original_shape[1]
                y1 = ((y - h/2) / 640) * original_shape[0]
                x2 = ((x + w/2) / 640) * original_shape[1]
                y2 = ((y + h/2) / 640) * original_shape[0]
                confidence = detections[i, 4]
                boxes.append([x1, y1, x2, y2, confidence])
        
        boxes = np.array(boxes)
 
        return boxes, original_image
 
    def draw_detections(self, image, detections):
        """
        Dibuja las detecciones en la imagen
        """
        result_image = image.copy()
        for det in detections:
            x1, y1, x2, y2 = det
            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)
            cv2.rectangle(result_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        return result_image
 
 
def preprocess_image(image):
 
    # Preprocesamiento
    # 1. Redimensionar con margen extra
    height, width = crop_image.shape[:2]
    # Añadir un pequeño borde para mejorar el reconocimiento
    crop_image = cv2.copyMakeBorder(crop_image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    # Redimensionar manteniendo el aspecto
    scale_factor = 200 / height if height < width else 200 / width
    enlarged = cv2.resize(crop_image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
    
    # 2. Conversión a escala de grises
    gray = cv2.cvtColor(enlarged, cv2.COLOR_BGR2GRAY)
    
    # 3. Mejora de contraste con ecualización de histograma
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    equalized = clahe.apply(gray)
    
    # 4. Reducción de ruido con filtro bilateral
    denoised = cv2.bilateralFilter(equalized, 11, 17, 17)
    
    # 5. Umbralización de Otsu (automática)
    _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 6. Dilatar ligeramente para conectar componentes de caracteres
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(binary, kernel, iterations=1)
    
    return dilated
 
# Ejemplo de uso
if __name__ == "__main__":
    model_path = sys.argv[1]
    image_path = sys.argv[2]

    # Inicializar detector
    detector = LicensePlateDetector(model_path)
    
    # Detectar matrículas
    start_time = time.time()
    detections, original_image = detector.detect(image_path)
    detections = detector.non_max_suppression(detections)
    end_time = time.time()
    print(f"Tiempo total de detección: {end_time - start_time} segundos")
 
    print(len(detections))
    
    # Dibujar resultados
    result_image = detector.draw_detections(original_image, detections)
    
    # Guardar resultados en lugar de mostrarlos
    cv2.imwrite("detecciones.jpg", result_image)
    # cv2.imshow("Detecciones", result_image) # Comentar esta línea
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
 
    reader = easyocr.Reader(['en'])
 
    start_time = time.time()
    #Recortamos las detecciones
    for i, det in enumerate(detections):
        x1, y1, x2, y2 = det
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        crop_image = original_image[y1:y2, x1:x2]
 
        # Guardar imagen original recortada
        cv2.imwrite(f"matricula_{i}_original.jpg", crop_image)
 
        # EasyOCR
        result = reader.readtext(crop_image)
        #union de detecciones
        # Sorteamos por la esquina superior izquierda
        result.sort(key=lambda x: x[0][0][0])
 
        texto = ""
        for detection in result:
            texto += detection[1]
        texto = texto.replace(" ", "")
        print(f"EasyOCR resultado: {texto}")
    end_time = time.time()
    print(f"Tiempo total de OCR: {end_time - start_time} segundos")