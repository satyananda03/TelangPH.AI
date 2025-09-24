import cv2
import numpy as np
import onnxruntime as ort
import os

# Load ONNX model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Lokasi file ini
MODEL_DIR = os.path.join(BASE_DIR, '..', 'models')     # app/models
PSPNet_model_onnx = os.path.join(MODEL_DIR, 'PSPNet_liquid_segmentation.onnx')
session = ort.InferenceSession(PSPNet_model_onnx, providers=["CPUExecutionProvider"])
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

def get_largest_mask(mask):
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return None, None
    largest_contour = max(contours, key=cv2.contourArea)
    largest_mask = np.zeros_like(mask)
    cv2.drawContours(
        largest_mask, [largest_contour], -1, 255, thickness=cv2.FILLED)
    return largest_mask, largest_contour


def get_segmented_object(image):
    segmented_object = None
    h, w, d = image.shape
    r = max(h, w)
    if r > 840:
        fr = 840 / r
        image = cv2.resize(image, (int(w * fr), int(h * fr)))
    # Preprocess: B x C x H x W, float32
    Im_tensor = image.astype(np.float32)
    Im_tensor = np.transpose(Im_tensor, (2, 0, 1))  # C x H x W
    Im_tensor = np.expand_dims(Im_tensor, axis=0)  # 1 x C x H x W
    # Run inference
    onnx_output = session.run([output_name], {input_name: Im_tensor})[
        0]  # shape: (1, H, W)
    Lb = onnx_output[0].astype(np.uint8)  # remove batch dimension → (H, W)
    if Lb.mean() > 0.001:
        largest_mask, largest_contour = get_largest_mask(Lb)
        if largest_mask is not None:
            largest_mask = largest_mask.astype(np.uint8)
            x, y, w_box, h_box = cv2.boundingRect(largest_contour)
            cropped_image = image[y:y + h_box, x:x + w_box]
            cropped_mask = largest_mask[y:y + h_box, x:x + w_box]
            # Terapkan mask ke gambar yang telah di-crop
            segmented_object = cv2.bitwise_and(cropped_image, cropped_image, mask=cropped_mask)
            if segmented_object.size == 0:
                segmented_object = None
    return segmented_object