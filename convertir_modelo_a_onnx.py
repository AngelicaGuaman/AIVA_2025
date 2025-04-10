import ultralytics

model = ultralytics.YOLO("license_plate_detector.pt")

#Convertir el modelo a onnx
model.export(format="onnx")
