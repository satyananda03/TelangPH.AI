from fastapi import File, UploadFile, HTTPException
import numpy as np
import cv2

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB in bytes

async def read_image(image: UploadFile = File(...)):
    # Validasi tipe MIME
    if image.content_type not in ['image/jpeg', 'image/jpg', 'image/png']:
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only JPG and PNG are allowed!")
    # Baca isi file (bytes)
    image_data = await image.read()
    # Validasi ukuran file
    if len(image_data) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400, detail="File size exceeds 5MB. Please upload a smaller image.")
    # Convert ke format OpenCV
    np_img = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    # Validasi kalau decoding gagal
    if img is None:
        raise HTTPException(
            status_code=400, detail="Could not decode the image.")
    return img