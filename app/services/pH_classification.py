import cv2
import numpy as np
import onnxruntime as ort
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Lokasi dari file ini
MODEL_DIR = os.path.join(BASE_DIR, '..', 'models')     # app/models
CNN_model_onnx = os.path.join(MODEL_DIR, 'TinySwinTransformer_pH_Classification.onnx')
session = ort.InferenceSession(CNN_model_onnx, providers=["CPUExecutionProvider"])
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name
# Normalisasi sesuai dataset
dataset_mean = np.array([0.2757323, 0.28446444, 0.33513261], dtype=np.float32)
dataset_std = np.array([0.21059035, 0.2042752, 0.22735262], dtype=np.float32)
# List of classes (pH values)
class_list = ['10', '11', '12', '13', '2', '3', '4', '5', '6', '7', '8', '9']

def get_pH_value(segmented_object):
    # Konversi BGR → RGB
    segmented_object = cv2.cvtColor(segmented_object, cv2.COLOR_BGR2RGB)
    # Resize ke (227, 227)
    segmented_object_resized = cv2.resize(segmented_object, (227, 227))
    # Konversi ke float32 dan normalisasi
    img = segmented_object_resized.astype(np.float32) / 255.0
    img = (img - dataset_mean) / dataset_std
    # Tambahkan dimensi batch → (1, 227, 227, 3)
    img = np.expand_dims(img, axis=0)
    # ONNX biasanya butuh format NCHW (1, 3, 227, 227), jadi transpose
    img = np.transpose(img, (0, 3, 1, 2))
    # Inference
    predictions = session.run([output_name], {input_name: img})[0]
    # Ambil class dengan probabilitas tertinggi
    predicted_class = np.argmax(predictions, axis=1)[0]
    predicted_pH = class_list[predicted_class]
    return predicted_pH