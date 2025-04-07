import onnxruntime
import cv2
import numpy as np

class Detector:
    def __init__(self, model_path="license_plate_detector.onnx", providers=['CPUExecutionProvider'], conf_threshold=0.5, iou_threshold=0.45):
        """
        Inicializa el detector de matrículas usando ONNX Runtime
        """
        # Configurar opciones para usar solo CPU
        self.session = onnxruntime.InferenceSession(model_path, providers=providers)
        
        # Obtener nombres de entrada/salida del modelo
        self.input_name = self.session.get_inputs()[0].name
        self.output_names = [output.name for output in self.session.get_outputs()]
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.initialized = True

    def preprocess_image(self, image, input_height=640, input_width=640):
        """
        Preprocesa la imagen para el modelo ONNX
        """
        # Redimensionar y preparar la imagen (ajustar según tu modelo)
        img = cv2.resize(image, (input_width, input_height))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Normalizar y cambiar formato
        img = img.astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1))  # HWC -> CHW
        img = np.expand_dims(img, axis=0)  # Añadir dimensión del batch
        
        return img
    
    def non_max_suppression(self, detections):
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
        indices = cv2.dnn.NMSBoxes(bboxes=boxes, scores=scores, score_threshold=self.conf_threshold, nms_threshold=self.iou_threshold)
        # Filter out the boxes based on the NMS result
        filtered_boxes = [boxes[i] for i in indices.flatten()]
        
        # Devolver las detecciones filtradas
        return filtered_boxes
    
    def process(self, image, original_image):
        """
        Procesa una lista de imágenes
        """
        """
        Detecta matrículas en la imagen
        """
            
        original_shape = original_image.shape

        # Inferencia
        outputs = self.session.run(self.output_names, {self.input_name: image})
        
        # Procesar resultados (ajustar según la salida de tu modelo)
        # Asumiendo que la salida tiene el formato [batch, num_detections, 6] 
        # donde 6 = [x1, y1, x2, y2, confidence, class]
        detections = np.transpose(outputs[0])
        
        # Filtrar por confianza
        boxes = []
        mask = detections[:, 4] >= self.conf_threshold
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

        return boxes



    def detect(self, lista_image_numpy_array):
        """
        Simula la detección de regiones en una imagen
        
        Args:
            lista_image_numpy_array (list): Lista de numpy arrays que representan imágenes
            
        Returns:
            list: Lista de regiones detectadas (simuladas)
        """
        
        results = []
        for image_numpy_array in lista_image_numpy_array:
            imagen_a_detectar = self.preprocess_image(image_numpy_array)
            resultados_procesados = self.process(imagen_a_detectar, image_numpy_array)
            resultados_procesados = self.non_max_suppression(resultados_procesados)
            results.append(resultados_procesados)
        return results
    