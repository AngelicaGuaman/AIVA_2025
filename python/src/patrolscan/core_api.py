from flask import Flask, request, jsonify
import cv2
import numpy as np
import os
from patrolscan.core import PatrolScan
from patrolscan.config import Config

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB

base_dir = os.path.dirname(os.path.abspath(__file__))
#model_path = os.path.join(base_dir, '..', '..', '..', 'modelos', 'license_plate_detector.onnx')
#model_path = os.path.join(base_dir, 'license_plate_detector.onnx')

model_path = 'license_plate_detector.onnx'

print(f"Exists: {os.path.exists(model_path)}")

config = Config()
config.modelo_detector_path = model_path
config.providers_onnx = ['CPUExecutionProvider']
config.conf_threshold_detector = 0.5
config.iou_threshold_detector = 0.45

patrolscan = PatrolScan(config=config)

# 413 Request Entity Too Large: 
# The data value transmitted exceeds the capacity limit.
@app.route('/patrolscan/api/v1/image-base64', methods=['POST'])
def scan_image():
    try:
        # Obtener la imagen en base64 del formulario multipart
        if 'image' not in request.form:
            return jsonify({"error": "Falta el campo 'image'"}), 400

        image_base64 = request.form['image']

        # Procesar la imagen con PatrolScan
        result = patrolscan.scan_base64(image_base64)

        # Retornar los resultados
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/patrolscan/api/v1/file', methods=['POST'])
def scan_image_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Falta el archivo 'file'"}), 400

        image_file = request.files['file']
        image_bytes = image_file.read()

        # Procesar el fichero con PatrolScan
        result = patrolscan.scan_bytes(image_bytes)

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/patrolscan/api/v1/files', methods=['POST'])
def scan_image_files():
    try:
        if 'files' not in request.files:
            return jsonify({"error": "Falta el archivo 'files'"}), 400

        image_files = request.files.getlist('files')  # Obtener la lista de archivos
        print(f"Files: {image_files}")
        image_files_byte = []
        results = []
        for file in image_files:
            image_bytes = file.read()
            image_files_byte.append(image_bytes)  # Agregar los bytes a la lista
        
        results = patrolscan.batch_scan_bytes(image_files_byte)

        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/patrolscan/api/v1/video', methods=['POST'])
def scan_video_file():
    try:
        if 'video' not in request.files:
            return jsonify({"error": "Falta el archivo 'video'"}), 400

        video_file = request.files['video']
        video_bytes = video_file.read()

        # Guardar el archivo temporalmente para procesarlo con OpenCV
        video_path = 'temp_video.mp4'
        with open(video_path, 'wb') as f:
            f.write(video_bytes)

        # Usar OpenCV para leer el video
        video = cv2.VideoCapture(video_path)
        all_results = []

        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break

            frame_rate = int(video.get(cv2.CAP_PROP_FPS))
            frame_interval = max(1, frame_rate // 2)  # Process every second frame

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
                if result:
                    all_results.extend(result) 

        video.release()
        cv2.destroyAllWindows()

        return jsonify(all_results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
