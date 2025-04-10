#pip install --upgrade torch ultralytics
#pip install easyocr
from ultralytics import YOLO
import cv2
from PIL import Image
import easyocr
import numpy as np

model = YOLO("yolov10n.pt")
results = model("data/ejemplo1.png")
results[0].show()

# Initialize EasyOCR reader
#reader = easyocr.Reader(['en'])
reader = easyocr.Reader(['en'], gpu=False)

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

                # Convert to format compatible with EasyOCR
                plate_image = Image.fromarray(binary_plate)
                plate_array = np.array(plate_image)

                # Use EasyOCR to read text from plate
                plate_number = reader.readtext(plate_array)
                concat_number = ' '.join([number[1] for number in plate_number])
                number_conf = np.mean([number[2] for number in plate_number]) if plate_number else 0

                if number_conf  > 0.7:
                    print(f"Detected Plate: {concat_number} with confidence {number_conf:.2f}")
                    # Draw the detected text on the frame
                    if plate_number:
                        cv2.putText(
                            img=frame,
                            text=f"Plate: {concat_number} ({number_conf:.2f})",
                            org=(r0, r1 - 10),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.7,
                            color=(0, 0, 255),
                            thickness=2
                        )

                else:
                    print("Low confidence in detected plate number.")
                
            except Exception as e:
                print(f"OCR Error: {e}")
                pass

    print(high_confidence_detections)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
