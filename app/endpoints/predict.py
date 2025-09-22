from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.liquid_segmentation import get_segmented_object
from app.services.pH_classification import get_pH_value
from app.services.process_image import read_image
from app.schemas.predict_schema import PredictResponse
# import time

predict_routes = APIRouter()

@predict_routes.post("/predict")
async def predict(name: str = Form(...), desc: str = Form(...), img: UploadFile = File(...)) -> PredictResponse:
    image = await read_image(img)
    # t_start = time.perf_counter()
    segmented_object = get_segmented_object(image)
    if segmented_object is None:
        raise HTTPException(
            status_code=400, detail="There is no Liquid on the Image!, please upload another Image")
    predicted_pH_value = get_pH_value(segmented_object)
    # total_time = time.perf_counter() - t_start
    return PredictResponse(name=name,
                            desc=desc,
                            pH_value=predicted_pH_value)
