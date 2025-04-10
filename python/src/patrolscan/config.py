

class Config:
    def __init__(self):
        self.modelo_detector_path = "license_plate_detector.onnx"
        self.providers_onnx = ['CPUExecutionProvider']
        self.conf_threshold_detector = 0.5
        self.iou_threshold_detector = 0.45


    def __str__(self):
        return f"Config(modelo_detector_path={self.modelo_detector_path}, providers_onnx={self.providers_onnx}, conf_threshold_detector={self.conf_threshold_detector}, iou_threshold_detector={self.iou_threshold_detector})"
