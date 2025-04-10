import onnxruntime as ort
import cv2
import numpy as np
import pytesseract
import easyocr
import time


class LicensePlateDetector:
    def __init__(self, model_path="license_plate_detector.onnx"):
        """
        Inicializa el detector de matrículas usando ONNX Runtime con CPU
        """
        # Configurar opciones para usar solo CPU
        providers = ['CUDAExecutionProvider']
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


def preprocess_for_tesseract(image):
    """
    Preprocesa la imagen para mejorar el reconocimiento con Tesseract
    """
    # Convertir a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Mejora de contraste
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    equalized = clahe.apply(gray)
    
    # Reducción de ruido
    denoised = cv2.bilateralFilter(equalized, 11, 17, 17)
    
    # Umbralización de Otsu
    _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Dilatación para conectar componentes
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(binary, kernel, iterations=1)
    
    return dilated

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

def evaluate_ocr_engines(image_path):
    """
    Evalúa diferentes motores OCR en las matrículas detectadas
    """
    # Inicializar detector
    detector = LicensePlateDetector("license_plate_detector.onnx")
    
    # Detectar matrículas
    print(f"Procesando imagen: {image_path}")
    start_time = time.time()
    detections, original_image = detector.detect(image_path)
    detections = detector.non_max_suppression(detections)
    detection_time = time.time() - start_time
    print(f"Tiempo de detección: {detection_time:.3f} segundos")
    print(f"Número de matrículas detectadas: {len(detections)}")
    
    # Inicializar motores OCR
    easyocr_reader = easyocr.Reader(['en'])
    
    # Dibujar y guardar resultados de detección
    result_image = detector.draw_detections(original_image, detections)
    cv2.imwrite("detecciones.jpg", result_image)
    
    # Procesar cada detección con diferentes OCRs
    results = []
    
    for i, det in enumerate(detections):
        x1, y1, x2, y2 = map(int, det)
        crop_image = original_image[y1:y2, x1:x2]
        
        # Guardar imagen original recortada
        cv2.imwrite(f"matricula_{i}_original.jpg", crop_image)
        
        print(f"\nProcesando matrícula #{i+1}:")
        ocr_results = {}
        
        # 1. EasyOCR con imagen original
        start_time = time.time()
        easyocr_original = easyocr_reader.readtext(crop_image)
        easyocr_original_time = time.time() - start_time
        
        easyocr_original_text = "".join([detection[1] for detection in sorted(easyocr_original, key=lambda x: x[0][0][0])]).replace(" ", "")
        ocr_results["easyocr_original"] = {
            "text": easyocr_original_text,
            "time": easyocr_original_time
        }
        print(f"EasyOCR (original): '{easyocr_original_text}' en {easyocr_original_time:.3f} segundos")
        
        # 2. EasyOCR con preprocesamiento
        preprocessed_easyocr = preprocess_for_easyocr(crop_image)
        cv2.imwrite(f"matricula_{i}_preprocesada_easyocr.jpg", preprocessed_easyocr)
        
        start_time = time.time()
        easyocr_preprocessed = easyocr_reader.readtext(preprocessed_easyocr)
        easyocr_preprocessed_time = time.time() - start_time
        
        easyocr_preprocessed_text = "".join([detection[1] for detection in sorted(easyocr_preprocessed, key=lambda x: x[0][0][0])]).replace(" ", "")
        ocr_results["easyocr_preprocessed"] = {
            "text": easyocr_preprocessed_text,
            "time": easyocr_preprocessed_time
        }
        print(f"EasyOCR (preprocesada): '{easyocr_preprocessed_text}' en {easyocr_preprocessed_time:.3f} segundos")
        
        # 3. Tesseract con imagen original
        start_time = time.time()
        tesseract_original_text = pytesseract.image_to_string(crop_image, config='--psm 7 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789').strip()
        tesseract_original_time = time.time() - start_time
        
        ocr_results["tesseract_original"] = {
            "text": tesseract_original_text,
            "time": tesseract_original_time
        }
        print(f"Tesseract (original): '{tesseract_original_text}' en {tesseract_original_time:.3f} segundos")
        
        # 4. Tesseract con preprocesamiento
        preprocessed_tesseract = preprocess_for_tesseract(crop_image)
        cv2.imwrite(f"matricula_{i}_preprocesada_tesseract.jpg", preprocessed_tesseract)
        
        start_time = time.time()
        tesseract_preprocessed_text = pytesseract.image_to_string(preprocessed_tesseract, config='--psm 7 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789').strip()
        tesseract_preprocessed_time = time.time() - start_time
        
        ocr_results["tesseract_preprocessed"] = {
            "text": tesseract_preprocessed_text,
            "time": tesseract_preprocessed_time
        }
        print(f"Tesseract (preprocesada): '{tesseract_preprocessed_text}' en {tesseract_preprocessed_time:.3f} segundos")
        
        results.append(ocr_results)
    
    return results

# Ejemplo de uso
if __name__ == "__main__":
    image_path = "dataset/20250131_155750/frames/frame2111.png"
    results = evaluate_ocr_engines(image_path)
    
    # Muestra un resumen
    print("\n=== RESUMEN DE RESULTADOS ===")
    for i, plate_results in enumerate(results):
        print(f"\nMatrícula #{i+1}:")
        for method, data in plate_results.items():
            print(f"  {method}: '{data['text']}' ({data['time']:.3f}s)")