from ultralytics import YOLO
import cv2
from PIL import Image
import pytesseract
import numpy as np

# Configura la ruta de Tesseract si no está en el PATH del sistema
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

model = YOLO("yolov10n.pt")
results = model("data/ejemplo1.png")
results[0].show()

frame_skip = 10
frame_count = 0

cap = cv2.VideoCapture("../data/20250203_132818.mp4")
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Skip frames
    if frame_count % frame_skip != 0:
        frame_count += 1
        continue  # Skip processing this frame

    results = model(frame)
    detections = results[0]

    high_confidence_detections = []
    for detection in detections.boxes.data.tolist():
        x1, y1, x2, y2, conf, cls = detection
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
       
        if conf > 0.9:
            label = f"{model.names[cls]} {conf:.2f}"  # Label with class name and confidence
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            high_confidence_detections.append({
                "class": model.names[cls],
                "confidence": conf,
                "bbox": (x1, y1, x2, y2)
            })

            # Try to apply OCR on detected region
            try:
                # Ensure coordinates are within frame bounds
                r0 = max(0, x1)
                r1 = max(0, y1)
                r2 = min(frame.shape[1], x2)
                r3 = min(frame.shape[0], y2)

                # Crop license plate region
                plate_region = frame[r1:r3, r0:r2]

                # Preprocess the cropped region for better OCR results
                gray_plate = cv2.cvtColor(plate_region, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
                enhanced_plate = cv2.bilateralFilter(gray_plate, 11, 17, 17)  # Reduce noise
                _, binary_plate = cv2.threshold(enhanced_plate, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Binarize

                # Use Tesseract to read text from plate
                plate_text = pytesseract.image_to_string(binary_plate, config='--psm 8')  # PSM 8: Treat image as a single word
                print(f"Detected Plate: {plate_text.strip()}")

                # Draw the detected text on the frame
                cv2.putText(
                    img=frame,
                    text=f"Plate: {plate_text.strip()}",
                    org=(r0, r1 - 10),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.7,
                    color=(0, 0, 255),
                    thickness=2
                )

            except Exception as e:
                print(f"OCR Error: {e}")
                pass

    print(high_confidence_detections)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()